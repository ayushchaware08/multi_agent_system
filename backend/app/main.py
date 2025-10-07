from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Manually tell dotenv where your .env file is
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=env_path)

from .api import ask, upload, logs

app = FastAPI(title="Multi-Agent Dynamic Decision System")

# print("Groq key loaded:", os.getenv("GROQ_API_KEY"))

# Key API Routes:
# /ask accepts a query and any PDF doc_id, routes to Controller.decide(), which selects an agent and returns {"answer": answer, "agent": agent, "trace": ...}.
# /upload_pdf accepts file, checks size, stores it, and performs inline PDF-to-Chroma ingestion (returns ingestion status).
# /logs returns decision logs for debugging.
# /ask accepts either query text or reference to uploaded PDF id — controller decides which agent to call and logs full reasoning + retrieved doc ids and timestamps.
# /logs returns recent decision logs (with filtering capability).
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])
