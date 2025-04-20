# logdoc/core/header_injector.py
import os
from pathlib import Path
from datetime import datetime
from logdoc.errors.logdoc_exceptions import HeaderInjectionError
from logdoc.logger import log_event

def get_file_metadata(file_path):
    stats = os.stat(file_path)
    created = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return created, modified
'''
def generate_header(filename, author, created, modified_by, modified_date):
    return f"""
Filename: {filename}
Author: {author}
Creation date: {created}
Last modified by: {modified_by}
Last modified date: {modified_date}
"""'''
def generate_header(filename, author, created, modified_by, modified_date):
    """
    Genereer een correcte triple-quoted Python headerblock.
    """
    return f'''""" 
Filename: {filename}
Author: {author}
Creation date: {created}
Last modified by: {modified_by}
Last modified date: {modified_date}
"""'''

def inject_logging_and_header(file_path, author="Unknown"):
    """
    Injecteert een header + log_event import in een Python bestand indien nodig.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        filename = os.path.basename(file_path)
        created, modified = get_file_metadata(file_path)
        header = generate_header(filename, author, created, author, modified)

        new_lines = lines[:]
        updated = False

        # Voeg header toe als die nog niet bestaat en niet al met triple quote begint
        if not any("Filename:" in line for line in lines[:7]) and (not lines or not lines[0].strip().startswith('"""')):
            new_lines.insert(0, header + "\n")
            updated = True

        # Voeg log_event import toe als die ontbreekt
        if not any("log_event" in line or "logutil" in line or "logdoc" in line for line in lines):
            insert_index = 0
            for idx, line in enumerate(new_lines):
                if line.startswith("import") or line.startswith("from"):
                    insert_index = idx + 1
            new_lines.insert(insert_index, "from logdoc.logger import log_event\n")
            updated = True

        if updated:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True
        return False

    except Exception as e:
        raise HeaderInjectionError(file_path, str(e))


def inject_headers(project_root, author="Unknown"):
    """
    Doorloopt een volledige mapstructuur en injecteert headers waar nodig.
    Retourneert een lijst met aangepaste bestanden.
    """
    updated_files = []
    for root, _, files in os.walk(project_root):
        if any(skip in root for skip in ["__pycache__", ".venv", "venv", "site-packages"]):
            continue
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                if inject_logging_and_header(full_path, author):
                    updated_files.append(full_path)
    return updated_files