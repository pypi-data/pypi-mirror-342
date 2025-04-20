import re
import os
import importlib.util

BORON_INIT = "boron/__init__.py"
CONFIG_FILE = "config.bn"
DOC_FILE = "boron_docs.md"

# Load boron package dynamically
def import_boron():
    spec = importlib.util.spec_from_file_location("boron", BORON_INIT)
    boron = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(boron)
    return boron

# Parse [C] section of config.bn
def parse_config():
    with open(CONFIG_FILE, "r") as f:
        lines = f.readlines()

    c_funcs = []
    parsing = False
    for line in lines:
        line = line.strip()
        if line == "[C]":
            parsing = True
            continue
        elif line.startswith("[") and parsing:
            break
        if parsing and line:
            path, func = line.split(":")
            c_funcs.append((path.strip(), func.strip()))
    return c_funcs

# Extract C function signature from source
def extract_func_signature(c_path, func_name):
    with open(c_path, "r") as f:
        code = f.read()

    pattern = re.compile(rf"([a-zA-Z_][a-zA-Z0-9_\*\s]+)\s+{func_name}\s*\(([^)]*)\)")
    match = pattern.search(code)

    if not match:
        return "int", []

    return_type = match.group(1).strip()
    args = match.group(2).strip()
    arg_list = []

    if args and args != "void":
        for arg in args.split(","):
            arg = arg.strip()
            if not arg:
                continue
            parts = arg.split()
            dtype = " ".join(parts[:-1]) if len(parts) > 1 else parts[0]
            arg_name = parts[-1] if len(parts) > 1 else "arg"
            arg_list.append((dtype.strip(), arg_name.strip()))

    return return_type, arg_list

# Generate documentation
def generate_docs():
    bn = import_boron()
    funcs = parse_config()

    # ✅ Fix: specify UTF-8 encoding to support emojis and special characters
    with open(DOC_FILE, "w", encoding="utf-8") as doc:
        doc.write("# 📄 Boron Function Documentation\n\n")

        for path, func in funcs:
            doc.write(f"## `{func}`\n")
            return_type, args = extract_func_signature(path, func)

            if hasattr(bn, func):
                doc_str = getattr(bn, func).__doc__
                description = f"This function returns a value of type {return_type}, accepts {args} as arguments"
            else:
                description = "⚠️ Function not found in boron module."

            # Write signature
            arg_str = ", ".join(f"{dtype} {name}" for dtype, name in args)
            signature = f"{return_type} {func}({arg_str})"

            doc.write(f"**Signature:** `{signature}`\n\n")
            doc.write(f"**Description:** {description}\n\n")
            doc.write("---\n\n")

if __name__ == "__main__":
    generate_docs()
