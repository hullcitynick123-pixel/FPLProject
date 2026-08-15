# FPL Project

A Streamlit dashboard for Premier League and Fantasy Premier League analytics.

## Prerequisites

- Python 3.10 or newer
- PowerShell on Windows
- An API-Football API key
- A publicly readable Google Sheet containing the project data

## Local Setup
py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual environment activation, allow it for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Configuration

Create a `.env` file in the repository root. The file is excluded from Git by `.gitignore`.

```env
API_FOOTBALL_KEY=your-api-football-key
WORK_SHEET_ID=your-google-sheet-id
WORK_SHEET_SQUADS=Current Squads
WORK_SHEET_TRANSFERS=Transfers
WORK_SHEET_TABLE=Scorecard
DEFAULT_LEAGUE_ID=39
DEFAULT_SEASON=2025
```

Replace the placeholder values with your own credentials and Google Sheet ID. Never commit `.env` or other secret files.

## Run the App

With the virtual environment activated:

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, usually <http://localhost:8501>.

To stop the app, press `Ctrl+C`. To leave the virtual environment:

```powershell
deactivate
```

## Project Structure

- `app.py` - Streamlit application entry point
- `config.py` - Environment and Streamlit secret configuration
- `api_client.py` - API-Football client
- `data_processor.py` - Google Sheets and data processing helpers
- `ceefax_theme/` - Dashboard styling and header components
- `utils/` - Date and news-feed utilities
- `requirements.txt` - Python dependencies
