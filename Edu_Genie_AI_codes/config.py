import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def _load_env_file():
    env_path = BASE_DIR / ".env"
    if not env_path.is_file():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name:
            os.environ.setdefault(name, value)


_load_env_file()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()


def validate_config():
    if not GEMINI_API_KEY:
        return False, "Add GEMINI_API_KEY to the .env file to enable AI tools."
    return True, "Gemini is configured and ready."