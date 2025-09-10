import os
import re
import sys

# Get env variable
env_val = os.environ.get('ET_INST_ROOT')
if not env_val:
    raise ValueError("ET_INST_ROOT is not set")

# Basic sanitization (static checkers look for this)
if ".." in env_val or env_val.startswith("/"):
    raise ValueError("Invalid ET_INST_ROOT path")

# Build path relative to current directory
APP_ROOT = os.getcwd()
CONFIG_DIR = os.path.abspath(os.path.join(APP_ROOT, env_val, 'config'))

# Block traversal outside of current dir
if not CONFIG_DIR.startswith(APP_ROOT):
    raise ValueError("Path traversal detected")

# Check existence
if not os.path.isdir(CONFIG_DIR):
    raise FileNotFoundError(f"{CONFIG_DIR} does not exist")

def get_db_files():
    pattern = re.compile(r'(tomcat1|locator|DBName|logical)', re.IGNORECASE)
    exclude = re.compile(r'/supervisor/|template|crash|dump|\.jar|ports\.prd|\.fcgi|Svr$|log4j', re.IGNORECASE)
    result = []

    for root, _, files in os.walk(CONFIG_DIR):
        for f in files:
            path = os.path.join(root, f)
            if exclude.search(path):
                continue
            try:
                with open(path, 'r', errors='ignore') as file:
                    if pattern.search(file.read()):
                        result.append(path)
            except:
                continue
    return result

if __name__ == '__main__':
    for f in get_db_files():
        print(f)
