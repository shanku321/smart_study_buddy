import os
import sqlite3
from sqlite3 import Error as SQLiteError
import streamlit as st


def get_level(score):

    if score >= 90:
        return "Expert"
    elif score >= 75:
        return "Hard"
    elif score >= 50:
        return "Medium"
    return "Easy"


def mastery_score(accuracy, consistency, retention):

    return round(
        (
         accuracy * 0.6
         + consistency * 0.2
         + retention * 0.2
        ), 2
    )

def get_latest_score():
    """Fetches the most recent quiz score and subject from the student_scores table.
    Returns:
        tuple: (score, subject) if found, or (None, None) if the table is empty.
    """
    try:
        # Secure absolute path anchoring
        #base_dir = os.path.dirname(os.path.abspath(__file__))

        # Note: If this script is inside a subfolder like 'services/', and your .db file
        # is in the main project root folder, change the line below to:
        # db_path = os.path.join(os.path.dirname(base_dir), "studybuddy.db")
        #db_path = os.path.join(base_dir, "studybuddy.db")

        with sqlite3.connect("studybuddy.db") as conn:
            cursor = conn.cursor()

            # Query to fetch the last inserted row ordered by id descending
            query = """
            SELECT score, subject 
            FROM student_scores
            where email = "shanku321@gmail.com"
            ORDER BY id DESC 
            LIMIT 1;
            """

            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return result[0], result[1]  # Returns (score, subject)
            return None, None

    except SQLiteError as e:
        print(f"Database error while fetching latest score: {e}")
        return None, None


