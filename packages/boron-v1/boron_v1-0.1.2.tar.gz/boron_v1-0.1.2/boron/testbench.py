import re
import os
import importlib.util
import ctypes

BORON_INIT = "boron/__init__.py"
CONFIG_FILE = "config.bn"

# Load boron package dynamically
def import_boron():
    spec = importlib.util.spec_from_file_location("boron", BORON_INIT)
    boron = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(boron)
    return boron

# C types to sample test values
type_to_sample = {
    "int": [0, 1, -1, 42],
    "float": [0.0, 1.1, -2.5, 3.14],
    "double": [0.0, 1.1, -2.5, 3.14],
    "char*": [b"hello", b"boron", b""],
    "char *": [b"hello", b"boron", b""],
}

# C types to ctypes
ctype_map = {
    "int": ctypes.c_int,
    "float": ctypes.c_float,
    "double": ctypes.c_double,
    "char*": ctypes.c_char_p,
    "char *": ctypes.c_char_p,
}

# Read [C] section of config.bn
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

# Extract the argument types and return type from a C function signature
def extract_func_signature(c_path, func_name):
    with open(c_path, "r") as f:
        code = f.read()

    pattern = re.compile(rf"([a-zA-Z_][a-zA-Z0-9_\*\s]+)\s+{func_name}\s*\(([^)]*)\)")
    match = pattern.search(code)

    if not match:
        print(f"Could not find declaration for {func_name} in {c_path}")
        return [], "int"  # Default return type

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
            arg_list.append(dtype.strip())

    return arg_list, return_type

# Run tests dynamically using sample values
def run_tests():
    bn = import_boron()
    funcs = parse_config()

    for path, func in funcs:
        print(f"\n🔧 Testing `{func}` from `{path}`")
        arg_types, return_type = extract_func_signature(path, func)

        if not hasattr(bn, func):
            print(f"⚠️ Function `{func}` not found in boron bindings.")
            continue

        func_ref = getattr(bn, func)

        # Set argument and return types
        try:
            func_ref.argtypes = [ctype_map.get(t, ctypes.c_int) for t in arg_types]
            func_ref.restype = ctype_map.get(return_type, ctypes.c_int)
        except Exception as e:
            print(f"⚠️ Couldn't set argtypes/restype for {func}: {e}")

        if not arg_types:
            try:
                result = func_ref()
                print(f"→ {func}() = {result}")
            except Exception as e:
                print(f"❌ Error calling {func}(): {e}")
            continue

        # Generate one test case per sample set
        sample_lists = [type_to_sample.get(t, [0]) for t in arg_types]
        test_args = zip(*sample_lists)

        for args in test_args:
            # Convert Python values to ctypes before passing
            ctypes_args = []
            for i, arg in enumerate(args):
                arg_type = arg_types[i]
                ctype = ctype_map.get(arg_type)
                if ctype is not None:
                    ctypes_args.append(ctype(arg))
                else:
                    ctypes_args.append(arg) # Fallback if type not found

            try:
                result = func_ref(*ctypes_args)
                display_args = [a.decode() if isinstance(a, bytes) else a for a in args]
                print(f"→ {func}({', '.join(map(str, display_args))}) = {result}")
            except Exception as e:
                display_args = [a.decode() if isinstance(a, bytes) else a for a in args]
                print(f"❌ Error calling {func}({', '.join(map(str, display_args))}): {e}")

if __name__ == "__main__":
    run_tests()