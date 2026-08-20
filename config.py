import os
#from anyio import Path
from pathlib import Path 
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
# Load Environment Variables
#load_dotenv()
# 1. Locate the root directory and load the .env file automatically
#BASE_DIR = Path(__file__).resolve().parent
#load_dotenv(BASE_DIR/".env")
#load_dotenv(find_dotenv(), override=True)
env_file = find_dotenv()
load_dotenv(env_file, override=True)

class Settings:
    # Gemini Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///studybuddy.db")

    # Application Settings
    APP_NAME: str = "Smart Study Buddy"
    MAX_CHUNK_SIZE: int = 1000
    TOP_K_RESULTS: int = 3
    SPACED_REPETITION_INTERVALS: list[int] = [1, 3, 7, 15, 30, 60]
    SUPPORTED_FILE_TYPES: list[str] = [
        ".pdf",
        ".txt",
        ".docx"
    ]
settings = Settings()

print(f"{settings.APP_NAME} Initialized Successfully")
#print(f"--- Environment Debug ---")
#print(f"Found .env file path: {env_file}")
#print(f"API Key loaded length: {len(settings.GOOGLE_API_KEY)} characters")
if not settings.GOOGLE_API_KEY:
    print("❌ CRITICAL WARNING: GOOGLE_API_KEY is empty inside .env!")
print(f"-------------------------")