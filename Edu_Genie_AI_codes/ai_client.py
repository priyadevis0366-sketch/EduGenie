import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import GEMINI_API_KEY, GEMINI_MODEL


RETRY_DELAYS = (1, 2)


def generate_text(prompt):
    if not GEMINI_API_KEY:
        raise ValueError("Gemini is not configured. Add GEMINI_API_KEY to the .env file.")

    model_name = GEMINI_MODEL.removeprefix("models/").strip("/")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model_name}:generateContent?{urlencode({'key': GEMINI_API_KEY})}"
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4},
    }).encode("utf-8")
    for attempt in range(len(RETRY_DELAYS) + 1):
        request = Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
            break
        except HTTPError as exc:
            try:
                error_body = json.loads(exc.read().decode("utf-8"))
                message = error_body.get("error", {}).get("message", "Request rejected")
            except (json.JSONDecodeError, UnicodeDecodeError):
                message = "Request rejected"

            if exc.code in (429, 503) and attempt < len(RETRY_DELAYS):
                time.sleep(RETRY_DELAYS[attempt])
                continue
            if exc.code == 503:
                raise RuntimeError(
                    "Gemini is still experiencing high demand after automatic retries. Please try again shortly."
                ) from None
            raise RuntimeError(f"Gemini API error ({exc.code}): {message}") from None
        except (URLError, TimeoutError) as exc:
            raise RuntimeError("Could not connect to the Gemini API. Check your network connection.") from exc
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise RuntimeError("Gemini returned an unreadable response.") from None

    candidates = result.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini did not return a response. Try changing the prompt.")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "\n".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text