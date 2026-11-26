import logging
import os
import time

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def call_llm(prompt: str, retries: int = 3) -> str:
    """
    Send a prompt to the configured LLM provider.
    Returns the response text. Raises on total failure.
    """
    for attempt in range(1, retries + 1):
        try:
            if AI_PROVIDER == "gemini":
                return _call_gemini(prompt)
            elif AI_PROVIDER == "groq":
                return _call_groq(prompt)
            else:
                raise ValueError(f"Unknown AI_PROVIDER: {AI_PROVIDER}")
        except Exception as e:
            wait = 2 ** attempt
            logger.warning(f"LLM attempt {attempt} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"LLM failed after {retries} attempts")


def _call_gemini(prompt: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text


def _call_groq(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
