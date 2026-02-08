#!/usr/bin/env python3
import argparse
import os
import sys
from scanner import scan

def main() -> int:
    parser = argparse.ArgumentParser(description = "A simple file integrity monitor")
    parser.add_argument("directory", help = "The root directory to scan")
    args = parser.parse_args()
    target_dir = os.path.abspath(os.path.expanduser(args.directory))

    if os.path.isdir(target_dir):
        print(f"[+] FIM targeting: {target_dir}")
        # Next step is pass to database and scanner
        files = scan(target_dir)
        for file in files:
            print(file)
        return 0
    else:
        print(f"[!] Error: {target_dir} is not a valid directory")
        return 1

if __name__== "__main__":
    sys.exit(main())
    
