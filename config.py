import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com").strip()
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587").strip())
EMAIL_USER = os.getenv("EMAIL_USER", "").strip()
EMAIL_PASS = os.getenv("EMAIL_PASS", "").strip()
EMAIL_TO = os.getenv("EMAIL_TO", "").strip()
EDITOR_NAME = os.getenv("EDITOR_NAME", "Hemal Mistry").strip()
EDITOR_TITLE = os.getenv("EDITOR_TITLE", "Editor-in-Chief, TechAi Samachar").strip()

def get_formatted_date(dt: datetime | None = None) -> str:
    """Returns date like 'Wednesday, November 18, 2026'."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%A, %B %d, %Y")

def get_short_date(dt: datetime | None = None) -> str:
    """Returns date like 'Nov 18, 2026'."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%b %d, %Y")

def get_month_label(dt: datetime | None = None) -> str:
    """Returns uppercase month like 'NOV' or 'MAYO' matching vintage newspaper stamps."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%b").upper()

def get_edition_number(start_str: str = "2026-01-01") -> int:
    """Calculates running edition number from reference start date."""
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        now = datetime.now()
        diff = (now - start).days
        return max(1, diff + 1)
    except Exception:
        return 1
