import os
from dotenv import load_dotenv

# Load .env at import time (EARLY)
load_dotenv(dotenv_path="backend/.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔥 LangSmith config
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

if not LANGSMITH_TRACING:
    raise ValueError("LANGSMITH_TRACING is not set in environment variables")

if not LANGSMITH_API_KEY:
    raise ValueError("LANGSMITH_API_KEY is not set in environment variables")

if not LANGSMITH_PROJECT:
    raise ValueError("LANGSMITH_PROJECT is not set in environment variables")
