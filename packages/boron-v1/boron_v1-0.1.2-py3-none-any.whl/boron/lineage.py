import os
import re
import sys
from datetime import datetime
import hashlib

CONFIG_FILE = "config.bn"
HISTORY_DIR = ".boron_history"

def parse_config():
    with open(CONFIG_FILE, "r") as f:
        lines = f.readlines()

    funcs = []
    current_lang = None
    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            current_lang = line[1:-1]
            continue
        if ":" in line and current_lang:
            path, func = line.split(":")
            funcs.append({
                "path": path.strip(),
                "func": func.strip(),
                "lang": current_lang
            })
    return funcs

def extract_c_function(filepath, func_name):
    with open(filepath, "r") as f:
        code = f.read()

    pattern = re.compile(rf"([a-zA-Z_][a-zA-Z0-9_\*\s]+)\s+{func_name}\s*\(([^)]*)\)\s*\{{(.*?)\}}", re.DOTALL)
    match = pattern.search(code)
    return match.group(0).strip() if match else None

def extract_py_function(filepath, func_name):
    with open(filepath, "r") as f:
        lines = f.readlines()

    func_def_index = None
    for i, line in enumerate(lines):
        if re.match(rf"\s*def\s+{func_name}\s*\(", line):
            func_def_index = i
            break

    if func_def_index is None:
        return None

    # Start collecting lines from the function definition
    func_lines = [lines[func_def_index]]
    indent_match = re.match(r"(\s*)", lines[func_def_index])
    base_indent = len(indent_match.group(1)) if indent_match else 0

    for line in lines[func_def_index + 1:]:
        # Stop if this line has less indentation and is not empty
        if line.strip() == "":
            func_lines.append(line)
            continue
        current_indent = len(re.match(r"(\s*)", line).group(1))
        if current_indent <= base_indent:
            break
        func_lines.append(line)

    return "".join(func_lines).rstrip()

def extract_function_code(filepath, func_name, lang):
    if lang == "C":
        return extract_c_function(filepath, func_name)
    elif lang == "PYTHON":
        return extract_py_function(filepath, func_name)
    else:
        print(f"[!] Unsupported language for {func_name}: {lang}")
        return None

def hash_content(content):
    return hashlib.sha256(content.encode()).hexdigest()

def save_lineage(func_name, path, lang, current_code):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    ext = os.path.splitext(path)[1].lstrip(".")
    filename = f"{func_name}__{os.path.basename(path)}.txt"
    file_path = os.path.join(HISTORY_DIR, filename)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            prev_code = f.read()
        if hash_content(prev_code) == hash_content(current_code):
            print(f"[✓] No change in `{func_name}` from {path}")
            return
        with open(file_path, "a") as f:
            f.write(f"\n\n# Update @ {now}\n")
            f.write(current_code)
        print(f"[+] Updated lineage for `{func_name}` at {file_path}")
    else:
        with open(file_path, "w") as f:
            f.write(f"# Initial snapshot @ {now}\n")
            f.write(current_code)
        print(f"[+] Created lineage for `{func_name}` at {file_path}")

def track_lineage(target_func=None):
    funcs = parse_config()
    for entry in funcs:
        if target_func and entry["func"] != target_func:
            continue
        path, func_name, lang = entry["path"], entry["func"], entry["lang"]
        if not os.path.exists(path):
            print(f"[!] Source not found: {path}")
            continue
        code = extract_function_code(path, func_name, lang)
        if code:
            save_lineage(func_name, path, lang, code)
        else:
            print(f"[!] Function `{func_name}` not found in {path}")

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    track_lineage(target_func=arg if arg not in ["lineage"] else None)
