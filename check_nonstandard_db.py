#!/usr/bin/env python3

import os
import re

ET_INST_ROOT = os.environ['ET_INST_ROOT']

def get_db_files():
    pattern = re.compile(r'(tomcat1|locator|DBName|logical)', re.IGNORECASE)
    exclude_patterns = re.compile(r'/supervisor/|template|crash|dump|\.jar|ports\.prd|\.fcgi|Svr$|log4j', re.IGNORECASE)

    matched_files = []
    config_path = os.path.join(ET_INST_ROOT, 'config')

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
            except Exception as e:
                # Could log the error or ignore
                continue

    return matched_files

def main():
    files = get_db_files()
    for f in files:
        print(f)

if __name__ == '__main__':
    main()
