import os
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

load_dotenv()

def format_url(raw: str) -> str:
    p = urlparse(raw, scheme="https")
    # move bare host into netloc
    if not p.netloc:
        p = p._replace(netloc=p.path, path="")
    # split & filter out empty segments
    parts = [seg for seg in p.path.split("/") if seg]
    # enforce “api” prefix and “v1” suffix
    if not parts or parts[0] != "api":
        parts.insert(0, "api")
    if parts[-1] != "v1":
        parts.append("v1")
    new_path = "/" + "/".join(parts) + "/"
    return urlunparse(p._replace(path=new_path))


DEFAULT_MODEL_NAME = os.getenv("OPENROUTER_MODEL_NAME",
                              os.getenv("MODEL_NAME", "google/gemini‑2.5‑pro…"))

BASE_URL = os.getenv("OPENROUTER_BASE_URL",
                     os.getenv("BASE_URL", "https://openrouter.ai/api/v1"))

BASE_URL = format_url(BASE_URL)

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is required")
