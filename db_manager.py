import sqlite3
import os
import traceback

# temporary import for testing without going through main.
from scanner import scan

# Get absolute path for the database
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "fim.db")

def initialize_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        try:
            print("--- Initializing Database ---")
            cursor = connection.cursor()

            baseline_query = '''
                CREATE TABLE IF NOT EXISTS baseline(
                    path TEXT PRIMARY KEY,
                    hash TEXT,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''

            current_scan_query = '''
                CREATE TABLE IF NOT EXISTS current_scan(
                    path TEXT PRIMARY KEY,
                    hash TEXT,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''
            
            paths_watched_query = '''
                CREATE TABLE IF NOT EXISTS paths_watched(
                    path TEXT PRIMARY KEY,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''
            cursor.execute(baseline_query)
            cursor.execute(current_scan_query)
            cursor.execute(paths_watched_query)

            connection.commit()
            print("[+] Database Initialized")
        
        except Exception as e:
            print(f"[-] Initialization failed: {e}")
            traceback.print_exc()



def populate_baseline(hash_list) -> None:
    pass

def populate_current_scan(hash_list) -> None:
    pass

def populate_paths_watched(path) ->

def diff_check() -> None:
    pass

def main():
    initialize_db()

if __name__ == "__main__":
    main()
