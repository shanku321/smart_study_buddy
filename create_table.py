import os
import sqlite3

try:
    # 1. Get the absolute path of the directory where this script lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "studybuddy.db")

    print(f"Attempting to create database at: {db_path}")

    # 2. Ensure all folders along this path actually exist
    os.makedirs(base_dir, exist_ok=True)

    # 3. Establish connection using the clean absolute path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 4. Execute your table creation logic
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        score INTEGER NOT NULL,
        subject TEXT NOT NULL,
        date_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("Success! 'studybuddy.db' and 'student_scores' created safely.")

except sqlite3.OperationalError as e:
    print(f"\nOperational Error: {e}")
    print("Tip: If you're using OneDrive, backup tools, or anti-virus folders, move your project folder to an open directory like C:\\projects")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
