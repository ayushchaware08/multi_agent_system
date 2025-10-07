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

# CRITICAL: Pre-load embedding model on startup
@app.on_event("startup")
async def startup_event():
    """
    Pre-load embedding model to avoid first-upload delay.
    This downloads the model once on startup (if not cached).
    """
    logger.info("="*60)
    logger.info("🔄 PRE-LOADING EMBEDDING MODEL...")
    logger.info("⏳ This may take 1-2 minutes on first run (downloading 133MB)")
    logger.info("="*60)
    
    try:
        from app.agents.pdf_rag import get_embeddings
        
        # Load model (will download if not cached)
        embeddings = get_embeddings()
        
        # Test it works
        test_embedding = embeddings.embed_query("test")
        
        logger.info("="*60)
        logger.info("✅ EMBEDDING MODEL LOADED AND READY!")
        logger.info(f"📊 Embedding dimension: {len(test_embedding)}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error("="*60)
        logger.error(f"❌ FAILED TO PRE-LOAD EMBEDDING MODEL: {e}")
        logger.error("⚠️  Uploads may be slow or fail!")
        logger.error("="*60)

# Register routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Multi-Agent System API is running"}

@app.get("/health")
async def health():
    """Health check with model status"""
    try:
        from app.agents.pdf_rag import get_embeddings
        get_embeddings()  # Check if model is loaded
        return {"status": "healthy", "embedding_model": "loaded"}
    except:
        return {"status": "degraded", "embedding_model": "not_loaded"}

logger.info("✅ All routers registered")
logger.info("✅ Backend initialization complete")
