import os
from dotenv import load_dotenv

load_dotenv()

def getenv(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

LLM_PROVIDER = getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = getenv("GROQ_API_KEY")
GROQ_MODEL = getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
OPENAI_MODEL = getenv("OPENAI_MODEL", "gpt-4o-mini")

EMBEDDINGS_PROVIDER = getenv("EMBEDDINGS_PROVIDER", "hf").lower()
HF_EMBEDDINGS_MODEL = getenv("HF_EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OPENAI_EMBEDDINGS_MODEL = getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")

CHROMA_DIR = getenv("CHROMA_DIR", "./chroma_db")
COLLECTION_NAME = getenv("COLLECTION_NAME", "support_kb")

TOP_K = int(getenv("TOP_K", "4"))
MIN_SCORE = float(getenv("MIN_SCORE", "0.35"))

ORDER_API_URL = getenv("ORDER_API_URL", "http://127.0.0.1:8000/order")
REFUND_API_URL = getenv("REFUND_API_URL", "http://127.0.0.1:8000/refund")