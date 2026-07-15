import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")


def _env_int(name: str, default: int = 0) -> int:
	raw = (os.getenv(name, str(default)) or str(default)).strip()
	try:
		return int(raw)
	except ValueError:
		return default


ADMIN_ID = _env_int("ADMIN_ID", 0)
REVIEW = _env_int("REVIEW", 0)


def _env(name: str, default: str = "") -> str:
	# Strip accidental trailing spaces from .env values (common with copied URLs).
	return (os.getenv(name, default) or default).strip()



WEBHOOK_URL = _env("WEBHOOK_URL")
SECRET_TOKEN = _env("SECRET_TOKEN")
TELEGRAM_WEBHOOK_PATH = _env("TELEGRAM_WEBHOOK_PATH", "/telegram/webhook")
