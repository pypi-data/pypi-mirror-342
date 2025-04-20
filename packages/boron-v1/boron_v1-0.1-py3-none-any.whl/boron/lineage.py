import os
import re
from datetime import datetime
import hashlib

CONFIG_FILE = "config.bn"
HISTORY_DIR = ".boron_history"

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

def extract_function_code(filepath, func_name):
    with open(filepath, "r") as f:
        code = f.read()

    pattern = re.compile(rf"([a-zA-Z_][a-zA-Z0-9_\*\s]+)\s+{func_name}\s*\(([^)]*)\)\s*\{{(.*?)\}}", re.DOTALL)
    match = pattern.search(code)

    if not match:
        return None
    return match.group(0).strip()

def hash_content(content):
    return hashlib.sha256(content.encode()).hexdigest()

def save_lineage(path, func_name, current_code):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    filename = f"{func_name}__{os.path.basename(path)}.txt"
    file_path = os.path.join(HISTORY_DIR, filename)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            prev_code = f.read()
        if hash_content(prev_code) == hash_content(current_code):
            return  # No change
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(file_path, "a") as f:
                f.write("\n\n# Update @ {}\n".format(now))
                f.write(current_code)
            print(f"[+] Updated lineage for `{func_name}` at {file_path}")
    else:
        with open(file_path, "w") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"# Initial snapshot @ {now}\n")
            f.write(current_code)
        print(f"[+] Created lineage for `{func_name}` at {file_path}")

def track_lineage():
    funcs = parse_config()
    for path, func_name in funcs:
        if not os.path.exists(path):
            print(f"[!] Source not found: {path}")
            continue
        code = extract_function_code(path, func_name)
        if code:
            save_lineage(path, func_name, code)
        else:
            print(f"[!] Function `{func_name}` not found in {path}")

if __name__ == "__main__":
    track_lineage()
