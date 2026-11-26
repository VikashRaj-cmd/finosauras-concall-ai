from dotenv import load_dotenv
load_dotenv(override=True)
import os
from groq import Groq

key = os.getenv("GROQ_API_KEY", "")
print(f"Using key: {key[:8]}...")
client = Groq(api_key=key)
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[{"role": "user", "content": "Say hello in one word."}],
    temperature=0.2,
)
print("Groq response:", response.choices[0].message.content)
