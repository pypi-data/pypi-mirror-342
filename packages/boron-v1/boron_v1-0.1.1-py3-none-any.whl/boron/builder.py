import os
import subprocess
import shutil
import sys
import importlib.util

sys.path.insert(0, os.path.abspath('.'))

def safe_remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"🧹 Removed old: {path}")
    except Exception as e:
        print(f"⚠️ Could not remove {path}: {e}")

WORKDIR = os.getcwd()
CONFIG_FILE = os.path.join(WORKDIR, "config.bn")
C_OUT = os.path.join(WORKDIR, "c_lib.dll")
INIT_FILE = os.path.join(WORKDIR, "__init__.py")

def parse_bn_file():
    sections = {"C": [], "PYTHON": [], "STRUCT": {}}
    current_lang = None

    with open(CONFIG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_lang = line[1:-1]
            elif current_lang == "STRUCT" and ":" in line:
                name, fields = map(str.strip, line.split(":"))
                field_list = [tuple(f.strip().split("=")) for f in fields.split(",")]
                sections["STRUCT"][name] = field_list
            elif ":" in line and current_lang:
                path, func = map(str.strip, line.split(":"))
                sections[current_lang].append((path, func))
    return sections

def build_c(c_sources):
    print("🔧 Building C...")
    files = " ".join([src for src, _ in c_sources])
    cmd = f"gcc -shared -o \"{C_OUT}\" -fPIC {files}"
    subprocess.run(cmd, shell=True, check=True)

def import_from_path(filepath):
    filepath = filepath.strip()
    abs_path = os.path.abspath(filepath)
    module_name = os.path.splitext(os.path.basename(abs_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    if spec is None:
        raise ImportError(f"Cannot load spec for {filepath}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def link_python(py_sources):
    print("🐍 Linking Python functions...")
    lines = []
    for path, func in py_sources:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            print(f"⚠️ Skipping {path}: File does not exist.")
            continue
        try:
            mod = import_from_path(abs_path)
            if not hasattr(mod, func):
                raise AttributeError(f"Function '{func}' not found in {path}")
            module_path = path.replace("/", ".").replace("\\", ".").removesuffix(".py")
            lines.append(f"from {module_path} import {func}")

        except Exception as e:
            print(f"⚠️ Skipping {func} from {path}: Import failed -> {e}")
    return lines

def generate_init(c_sources, py_lines, structs):
    boron_pkg_dir = os.path.join(WORKDIR, "boron")
    os.makedirs(boron_pkg_dir, exist_ok=True)

    relocated_dll = os.path.join(boron_pkg_dir, "c_lib.dll")
    relocated_init = os.path.join(boron_pkg_dir, "__init__.py")

    print("🧩 Generating __init__.py...")
    lines = []

    if structs:
        lines.append("import ctypes")
        for struct_name, fields in structs.items():
            lines.append(f"class {struct_name}(ctypes.Structure):")
            lines.append("    _fields_ = [")
            for fname, ftype in fields:
                if "[" in ftype and "]" in ftype:  # e.g. char[50]
                    base, count = ftype.replace("]", "").split("[")
                    ctype = f"ctypes.c_{base} * {count}"
                else:
                    ctype = f"ctypes.c_{ftype}"
                lines.append(f"        ('{fname}', {ctype}),")
            lines.append("    ]\n")

    if c_sources:
        lines += [
            "import ctypes",
            "import os",
            'c_lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "c_lib.dll"))',
            "",
        ]
        for _, func in c_sources:
            lines.append(f"def {func}(*args):")
            lines.append(f"    return c_lib.{func}(*args)")
            lines.append("")

    lines += py_lines

    with open(relocated_init, "w") as f:
        f.write("\n".join(lines))

    shutil.move(C_OUT, relocated_dll)
    print("📦 Moved output to boron/ package folder.")

# 🔨 Clean, callable build logic
def build():
    safe_remove(C_OUT)
    safe_remove(INIT_FILE)

    print("🚀 Building Boron...")
    if not os.path.exists(CONFIG_FILE):
        print("❌ config.bn not found in this folder.")
        return

    sections = parse_bn_file()

    if sections["C"]:
        build_c(sections["C"])

    py_lines = []
    if sections["PYTHON"]:
        py_lines = link_python(sections["PYTHON"])

    generate_init(sections["C"], py_lines, sections["STRUCT"])

# 🚀 CLI entry point (called from console)
def main():
    if len(sys.argv) < 2:
        print("Usage: boron [build|test]")
        return

    command = sys.argv[1]

    if command == "build":
        build()
    elif command == "test":
        try:
            sys.path.insert(0, os.getcwd())  # So we can import local files
            import testbench
            #from boron import __init__ as boron_module
            testbench.run_tests()
        except ImportError as e:
            print(f"❌ Import failed: {e}")
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
    elif command == "doc":
        try:
            sys.path.insert(0, os.getcwd())  # So we can import local files
            import docgen
            #from boron import __init__ as boron_module
            docgen.generate_docs()
        except ImportError as e:
            print(f"❌ Import failed: {e}")
    elif command == "lineage":
        try:
            sys.path.insert(0, os.getcwd())
            import lineage
            funcname = sys.argv[2] if len(sys.argv) > 2 else None
            lineage.track_lineage(funcname)
        except ImportError as e:
            print(f"❌ Import failed: {e}")
        except Exception as e:
            print(f"❌ Lineage tracking failed: {e}")

    else:
        print(f"❌ Unknown command: {command}")
