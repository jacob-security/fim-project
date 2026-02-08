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
                    hash TEXT
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


# This not only populates but also updates the baseline table
def populate_baseline(hash_list) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        try:
            print("--- Populating baseline table ---")
            cursor = connection.cursor()

            query = '''
                INSERT INTO baseline (path, hash)
                VALUES (?, ?)
                ON CONFLICT(path)
                DO UPDATE SET
                    hash = excluded.hash,
                    last_seen = CURRENT_TIMESTAMP;
            '''
            
            cursor.executemany(query, hash_list)
            connection.commit()
            print("[+] Success: baseline table populated")
        except Exception as e:
            print(f"[-] Error populating baseline table: {e}")
            traceback.print_exc()


def populate_current_scan(hash_list) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        try:
            print("--- Populating current_scan table ---")
            cursor = connection.cursor()
            
            # Clear the current scan table before populating
            cursor.execute("DELETE FROM current_scan")

            query = '''
                INSERT INTO current_scan (path, hash)
                VALUES (?, ?)
            '''

            cursor.executemany(query, hash_list)
            connection.commit()
        except Exception as e:
            print(f"[-] Error populating current_scan table: {e}")
            traceback.print_exc()



def populate_paths_watched(path) -> None:

    full_path = os.path.abspath(os.path.expanduser(path))
    with sqlite3.connect(DB_PATH) as connection:
        try:
            print("--- Populating paths_watched table ---")
            cursor = connection.cursor()
            
            query = '''
                INSERT INTO paths_watched (path, last_seen)
                VALUES (?, CURRENT_TIMESTAMP)
                ON CONFLICT(path)
                DO UPDATE SET last_seen = CURRENT_TIMESTAMP
            '''

            cursor.execute(query, (full_path,))
            connection.commit()
            print("[+] Success: populated paths_watched table")
        except Exception as e:
            print(f"[-] Error populating paths_watched table {e}")



def detect_modifications() -> list:
    with sqlite3.connect(DB_PATH) as connection:
        try:
            print("--- Detecting Modifications ---")
            cursor = connection.cursor()

            query = '''
                SELECT b.path
                FROM baseline as b
                JOIN current_scan c USING(path)
                WHERE b.hash != c.hash
            '''

            cursor.execute(query)

            print("[+] Success detecting modifications")
            modified_list = cursor.fetchall()
            if modified_list:
                print("[!] The following files were modified:")
                for item in modified_list:
                    print(item)
                return(modified_list)
            else:
                print("[+] No modifications detected")
                return []
        except Exception as e:
            print(f"[-] Error detecting modifications {e}")

def main():
    test_path = "./test_directory" 
    #initialize_db()
    hash_list = scan(test_path)
    #populate_baseline(hash_list)
    populate_current_scan(hash_list)
    populate_paths_watched(test_path)
    detect_modifications()

if __name__ == "__main__":
    main()
