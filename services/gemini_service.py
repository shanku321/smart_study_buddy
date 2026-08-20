import google.generativeai as genai

from config import Settings

model = genai.GenerativeModel(Settings.MODEL_NAME)
genai.configure(api_key=Settings.GOOGLE_API_KEY) 

def ask_gemini(prompt):

    response = model.generate_content(prompt)

    return response.text