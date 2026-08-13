import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import streamlit as st
    USE_STREAMLIT_SECRETS = True
except (ImportError, RuntimeError):
    USE_STREAMLIT_SECRETS = False

BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Load environment variables from .env file
env_path: Path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

def get_secret(key: str, default: str = "") -> str:
    """Get secret from Streamlit secrets or environment variables."""
    if USE_STREAMLIT_SECRETS:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except:
            return os.getenv(key, default)
    return os.getenv(key, default)

# API Credentials & Endpoints
API_KEY: str = get_secret("API_FOOTBALL_KEY", "")
BASE_URL: str = "https://v3.football.api-sports.io"

# Default FPL Settings
DEFAULT_LEAGUE_ID: int = int(get_secret("DEFAULT_LEAGUE_ID", "39"))
DEFAULT_SEASON: int = int(get_secret("DEFAULT_SEASON", "2025"))

# Work Sheet Details
SHEET_ID: str = get_secret("WORK_SHEET_ID", "")
SHEET_NAME: str = get_secret("WORK_SHEET_SQUADS", "Current Squads")