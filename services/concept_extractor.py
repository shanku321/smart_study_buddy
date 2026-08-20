from services.gemini_service import ask_gemini

def extract_concepts(content):

    prompt = f"""
    Extract:

    1. Main Concepts
    2. Definitions
    3. Important Points

    Return JSON

    Content:
    {content}
    """

    return ask_gemini(prompt)