#!/usr/bin/env python3

import os
import subprocess
import sys

ET_INST_ROOT = os.environ.get('ET_INST_ROOT')
if not ET_INST_ROOT:
    raise ValueError("ET_INST_ROOT not set")

# Make sure the directory exists
config_dir = os.path.join(ET_INST_ROOT, 'config')
if not os.path.isdir(config_dir):
    raise FileNotFoundError(f"Config directory does not exist: {config_dir}")

# Build the find command
find_cmd = [
    'find', config_dir, '-type', 'f', '-exec',
    'egrep', '-il', 'tomcat1|locator|DBName|logical', '{}', '+'
]

# Run find + grep (no shell=True)
try:
    find_proc = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Second grep to exclude unwanted files
    exclude_patterns = '/supervisor/|template|crash|dump|.jar|ports.prd|.fcgi|Svr$|log4j'
    grep_cmd = ['egrep', '-v', exclude_patterns]

    grep_proc = subprocess.Popen(grep_cmd, stdin=find_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    find_proc.stdout.close()  # Allow find_proc to receive SIGPIPE if grep_proc exits

    output, _ = grep_proc.communicate()

    files = output.decode().splitlines()

except Exception as e:
    print(f"Error during file scan: {e}", file=sys.stderr)
    files = []

def main():
    for f in files:
        print(f)

if __name__ == '__main__':
    main()
