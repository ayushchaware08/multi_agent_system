from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("🚀 Starting Multi-Agent System Backend...")

# Load environment
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=env_path)
logger.info(f"📂 Loaded .env from: {env_path}")

# Import routers
from .api import ask, upload, logs

# Create app
app = FastAPI(title="Multi-Agent Dynamic Decision System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NO STARTUP EVENT - Model loads on first use

# Register routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Multi-Agent System API is running"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "message": "Service is running"}

logger.info("✅ All routers registered")
logger.info("✅ Backend initialization complete")
