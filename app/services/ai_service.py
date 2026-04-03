from google import genai
from app.core.config import settings

# 1. Check for the API key
if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

# 2. Initialize the new Client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    """
    Sends a prompt to Gemini using the new SDK and returns the text response.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"