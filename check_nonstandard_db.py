#!/usr/bin/env python3

import os
import re
import sys
import pwd

# Get ET_INST_ROOT from environment
ET_INST_ROOT = os.environ.get('ET_INST_ROOT')
if not ET_INST_ROOT:
    print("ET_INST_ROOT is not set.", file=sys.stderr)
    sys.exit(1)

# Resolve config directory path
config_path = os.path.realpath(os.path.join(ET_INST_ROOT, 'config'))

# Check if config directory exists
if not os.path.isdir(config_path):
    print(f"Invalid ET_INST_ROOT: config directory not found at {config_path}", file=sys.stderr)
    sys.exit(1)

# Optional: check for dangerous base paths
forbidden_roots = ['/', '/etc', '/bin', '/usr', '/var', '/dev', '/proc']
if os.path.realpath(ET_INST_ROOT) in forbidden_roots:
    print("Security violation: ET_INST_ROOT points to a forbidden path", file=sys.stderr)
    sys.exit(1)

# Optional: check ownership of the config dir
try:
    config_stat = os.stat(config_path)
    current_uid = os.getuid()
    if config_stat.st_uid != current_uid:
        owner = pwd.getpwuid(config_stat.st_uid).pw_name
        print(f"Security warning: config dir owned by {owner}, not current user.", file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Error checking config dir ownership: {e}", file=sys.stderr)
    sys.exit(1)

def get_db_files():
    pattern = re.compile(r'(tomcat1|locator|DBName|logical)', re.IGNORECASE)
    exclude_patterns = re.compile(r'/supervisor/|template|crash|dump|\.jar|ports\.prd|\.fcgi|Svr$|log4j', re.IGNORECASE)

    matched_files = []

    MAX_DEPTH = 5

    for root, dirs, files in os.walk(config_path):
        depth = root[len(config_path):].count(os.sep)
        if depth > MAX_DEPTH:
            continue

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
                continue  # Skip unreadable files

    return matched_files

def main():
    files = get_db_files()
    for f in files:
        print(f)

if __name__ == '__main__':
    main()
