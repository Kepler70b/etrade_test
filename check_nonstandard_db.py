#!/usr/bin/env python3

import os
import re
import sys

# Define allowed root (can also be dynamic if validated)
APP_ROOT = os.getcwd()

def is_path_safe(user_path):
    # Allow only alphanumeric + dashes/underscores/slashes
    safe_pattern = re.compile(r'^[\w\-/]+$')
    if not safe_pattern.match(user_path):
        return False

    # Resolve and prevent access to forbidden paths
    resolved = os.path.realpath(user_path)
    for forbidden in ['/', '/etc', '/bin', '/usr', '/dev', '/proc', '/var']:
        if resolved == forbidden or resolved.startswith(forbidden + os.sep):
            return False
    return True

ET_INST_ROOT = os.environ.get('ET_INST_ROOT')
if not ET_INST_ROOT or not is_path_safe(ET_INST_ROOT):
    raise ValueError("ET_INST_ROOT is invalid or unsafe")

# Restrict to application subdirectory
safe_root = os.path.normpath(os.path.join(APP_ROOT, ET_INST_ROOT))
if not safe_root.startswith(APP_ROOT):
    raise ValueError("ET_INST_ROOT attempts directory traversal")

config_path = os.path.join(safe_root, 'config')
if not os.path.isdir(config_path):
    raise FileNotFoundError(f"{config_path} does not exist")

def get_db_files():
    pattern = re.compile(r'(tomcat1|locator|DBName|logical)', re.IGNORECASE)
    exclude_patterns = re.compile(r'/supervisor/|template|crash|dump|\.jar|ports\.prd|\.fcgi|Svr$|log4j', re.IGNORECASE)

    matched_files = []

    for root, dirs, files in os.walk(config_path):
        for file in files:
            filepath = os.path.join(root, file)
            if exclude_patterns.search(filepath):
                continue
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                    if pattern.search(content):
                        matched_files.append(filepath)
            except Exception:
                continue  # Ignore unreadable files

    return matched_files

def main():
    files = get_db_files()
    for f in files:
        print(f)

if __name__ == '__main__':
    main()
