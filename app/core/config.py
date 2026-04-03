import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Indian Law Bot API"
    # Fetch the API key, or return None if it's missing
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    
    # We can add more settings here later, like ChromaDB paths
    VECTOR_DB_PATH: str = "./data/vector_store"

# Create a global instance to use throughout the app
settings = Settings()