from dotenv import load_dotenv
load_dotenv()
from app.services.ai_service import get_ai_response
print("Calling AI...")
print(get_ai_response("Hello"))
print("Done AI")
