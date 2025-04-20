# logdoc/core/fix_headers.py
import os

HEADER_KEYS = ["Filename:", "Author:", "Creation date:", "Last modified by:", "Last modified date:"]

def is_flat_header(lines):
    return all(any(key in line for line in lines[:7]) for key in HEADER_KEYS)

def already_wrapped(lines):
    return lines[0].strip().startswith('"""') and any('"""' in line for line in lines[1:7])

def wrap_header_block(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not is_flat_header(lines) or already_wrapped(lines):
        return False

    insert_idx = next((i for i, line in enumerate(lines) if any(k in line for k in HEADER_KEYS)), 0)
    header_end = insert_idx + sum(1 for line in lines[insert_idx:] if any(k in line for k in HEADER_KEYS))

    # Wrap the header block
    header = lines[insert_idx:header_end]
    wrapped = ['"""\n'] + header + ['"""\n']
    new_lines = lines[:insert_idx] + wrapped + lines[header_end:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return True

def fix_all_headers(path):
    updated = []
    for root, _, files in os.walk(path):
        if any(ignored in root for ignored in [".venv", "venv", "__pycache__"]):
            continue
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                if wrap_header_block(full_path):
                    updated.append(full_path)
    return updated
