import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")