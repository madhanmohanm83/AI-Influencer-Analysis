import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

PROJECT_NAME = "Creator Intelligence Pro"

DATABASE_PATH = "data/creator_intelligence.db"

MAX_SEARCH_RESULTS = 50
