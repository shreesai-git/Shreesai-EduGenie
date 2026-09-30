import os
from dotenv import load_dotenv
from functools import lru_cache

try:
    from google import genai
except ImportError:  # pragma: no cover
    genai = None

load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"

@lru_cache(maxsize=1)
def get_client():
    if genai is None:
        raise RuntimeError("google-genai is not installed. Run: pip install -r requirements.txt")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")
    return genai.Client(api_key=api_key)

def generate(prompt: str, *, model: str | None = None, temperature: float = 0.4, max_output_tokens: int = 2048) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        contents=prompt,
        config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        },
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
