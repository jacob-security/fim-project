import argparse
import os
import sys
from scanner import scan
from db_manager import *

def main() -> int:
    parser = argparse.ArgumentParser(description = "A simple file integrity monitor")

    subparser = parser.add_subparsers(dest="command", help="FIM modes of operation")
    
    # --- MODE 1: Baseline ---
    baseline_parser = subparser.add_parser("baseline", help="create a new baseline")
    baseline_parser.add_argument("path", help="The file or directory to hash")

    # -- MODE 2: Scan ---
    scan_parser = subparser.add_parser("scan", help="Scan all watched paths for changes")

    args = parser.parse_args()
    
    
    initialize_db()

    if args.command == "baseline":
        # Access and get absolute path for root directory    
        target_dir = os.path.abspath(os.path.expanduser(args.path))

        if os.path.isdir(target_dir):
            print(f"--- Creating baseline for {target_dir} ---")
            # Next step is pass to database and scanner
            files = scan(target_dir)
            populate_baseline(files)
            populate_paths_watched(target_dir)
            print(f"[+] Success: baseline created for {target_dir}")
            return 0 
        else:
            print(f"[!] Error: {target_dir} is not a valid directory")
            return 1
    
    if args.command == "scan":
        print("--- Scanning all paths watched for file modifications ---")
        paths_watched = retrieve_paths_watched()
        
        # Flag to detect modifications to give user update option
        modified = False
        for path in paths_watched:
            hash_list = scan(path)
            populate_current_scan(hash_list)
            modified_files = detect_modifications()
            if modified_files:
                modified = True

        if modified:
            update_option = input("Would you like to update the baseline table with the current modifications? (y/N)")
            if update_option.lower() == 'y':
                for path in paths_watched:
                    files = scan(path)
                    populate_baseline(files)
            else:
                return 0

             

if __name__== "__main__":
    sys.exit(main())
    
