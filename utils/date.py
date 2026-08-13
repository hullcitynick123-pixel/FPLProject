from datetime import datetime

def get_current_date() -> str:
    """Return the current date in 'Day DD Mon HH:MM:SS' format."""
    return datetime.now().strftime("%a %d %b %H:%M:%S")