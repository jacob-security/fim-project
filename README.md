File Integrity Monitor

A Python-based security tool designed to monitor directory integrity by baselining and scanning files using cryptographic hashes stored in a SQLite database.
🚀 Features

    Baseline Generation: Walk through a directory and record the unique hash of every file.

    Integrity Scanning: Compare current file states against the baseline to detect additions, deletions, and modifications.

    Interactive Updates: When changes are detected, the user is prompted to accept the changes as the new baseline.

    Persistent Storage: Uses SQLite to store file metadata and hashes.

🛠 Usage
1. Create a Baseline

To capture the initial state of a directory, run:

python main.py baseline [directory]

Example: python main.py baseline /home/user/documents
2. Scan for Changes

To compare the current directory state against your saved baseline:

python main.py scan
3. Interactive Response

If the scan detects a mismatch, addition, or deletion, the script will prompt you:

    "Would you like to update the baseline table with the current modifications? (y/N)"

    Selecting 'y': The script will refresh the database table to reflect the current state of the files.

    Selecting 'N' (Default): No changes will be made to the database, allowing you to investigate the discrepancy.

⚠️ Safety Warning

Run with caution. If you execute this script with elevated permissions (e.g., sudo), it has the capability to read and process sensitive system files. Always test on non-critical directories before scanning system-level paths.
🛑 Current Limitations

    Table Refresh Logic: Currently, the script does not perform "delta updates" (updating only the specific fields where hashes changed). Instead, it updates the entire table when the user confirms an update.

    Performance: Scanning very large directories may take time depending on your hardware.

📘 Learning Objectives

This project was built to practice:

    Data Integrity: Understanding how hashing ensures files haven't been tampered with.

    User Interaction: Implementing conditional logic based on user input (y/N).

    Database Management: Using Python to interact with SQLite.
