import logging
import os
import time

from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger(__name__)


def call_llm(prompt: str, retries: int = 3) -> str:
    """
    Send a prompt to the configured LLM provider.
    Returns the response text. Raises on total failure.
    """
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    for attempt in range(1, retries + 1):
        try:
            if provider == "groq":
                return _call_groq(prompt)
            else:
                return _call_gemini(prompt)
        except Exception as e:
            wait = 2 ** attempt
            logger.warning(f"LLM attempt {attempt} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"LLM failed after {retries} attempts")


def _call_gemini(prompt: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text


def _call_groq(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800,
    )
    return response.choices[0].message.content
