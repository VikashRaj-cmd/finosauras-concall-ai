from dotenv import load_dotenv
load_dotenv(override=True)
import os
print("AI_PROVIDER:", os.getenv("AI_PROVIDER"))
print("GROQ_API_KEY set:", bool(os.getenv("GROQ_API_KEY")))
print("GEMINI_API_KEY set:", bool(os.getenv("GEMINI_API_KEY")))
