import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Load environment variables from .env file
env_path: Path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# API Credentials & Endpoints
API_KEY: str = os.getenv("API_FOOTBALL_KEY", "")
BASE_URL: str = "https://v3.football.api-sports.io"

# Default FPL Settings
DEFAULT_LEAGUE_ID: int = int(os.getenv("DEFAULT_LEAGUE_ID", 39))  # Premier League
DEFAULT_SEASON: int = int(os.getenv("DEFAULT_SEASON", 2025))     # 2025 for testing, switch to 2026 on Aug 21