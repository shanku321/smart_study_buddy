from datetime import datetime, timedelta
#from xml.parsers.expat import model

from dbm import sqlite3
import os
from flask import json
from langchain_community.vectorstores import FAISS  
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from config import settings  # 👈 Import your global config environment

INTERVALS = settings.SPACED_REPETITION_INTERVALS

def next_review(correct_count):
    if correct_count < len(INTERVALS):
        return (
                datetime.now()
                + timedelta(
                    days=INTERVALS[correct_count]
                )
        )
    return (
            datetime.now()
            + timedelta(days=90)
    )



# def generate_quiz(topic: str) -> str:
#     try:
#         # Configuration is automatically managed here!
#         genai.configure(api_key=settings.GOOGLE_API_KEY)
        
#         model = genai.GenerativeModel("gemini-2.5-flash")

#         # 3. Formulate your prompt
#         prompt = f"Create a 5-question multiple choice quiz about: {topic}. Provide answers."
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"


def generate_quiz(topic: str) -> str:
    try:
        # 1. Configure the Gemini API
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # 2. Initialize your embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # 3. Load your local FAISS vector database
        # Make sure 'doc_index' matches the folder name used when saving
        db_directory = "doc_index"  # Adjust this path if needed
        
        # ✅ FAISS requires 'allow_dangerous_deserialization=True' to load local files safely
        vector_db = FAISS.load_local(
            folder_path=db_directory, 
            embeddings=embeddings,
            allow_dangerous_deserialization=True  
        )

        # 4. Search the FAISS database for text chunks matching the topic
        docs = vector_db.similarity_search(topic, k=3)
        retrieved_context = "\n\n".join([doc.page_content for doc in docs])

        if not retrieved_context.strip():
            retrieved_context = "No relevant local documents found for this topic."

        # 5. Formulate your prompt using the retrieved context
        prompt = f"""
        You are an expert study assistant. Create a 10-question multiple choice quiz about the topic: "{topic}".
        
        Use the following retrieved context from the user's uploaded study materials to ground your questions and answers. Do not make up facts outside the context if it provides the information.
        
        Context:
        {retrieved_context}
        
        You MUST return 10-question multiple choice quiz about the topic.
        Give four options A, B, C, D for each question. Provide the correct answers and a brief explanation at the very end.
        """

        # 6. Generate the content using Gemini
        response = model.generate_content(prompt)        
        return response.text        

    except Exception as e:
        return f"Error generating quiz: {e}"


def insert_score(name: str, email: str, score: int, subject: str):
    """
    Inserts a student's quiz results into the student_scores table.
    """
    try:
        # Get the absolute path to ensure it connects to the correct database file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "studybuddy.db")
        
        # Connect to SQLite
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # SQL Insert query
            query = """
            INSERT INTO student_scores (name, email, score, subject)
            VALUES (?, ?, ?, ?);
            """
            
            # Execute with parameterized inputs for safety
            cursor.execute(query, (name, email, score, subject))
            conn.commit()
            return True
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False