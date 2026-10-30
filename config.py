
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Local .env first; Streamlit Cloud secrets as fallback
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    try:
        YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    except (KeyError, FileNotFoundError):
        YOUTUBE_API_KEY = None

PROJECT_NAME = "Creator Intelligence Pro"

DATABASE_PATH = "data/creator_intelligence.db"

MAX_SEARCH_RESULTS = 50
