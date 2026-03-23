import os
import json
import logging
from langchain_groq import ChatGroq
from app.utils.logging_utils import append_raw_log
from app.agents.pdf_rag import _vectorstore

logger = logging.getLogger(__name__)

# Print for debugging
# print("🔑 GROQ_API_KEY (from env at controller):", os.getenv("GROQ_API_KEY"))

GROQ_KEY = os.getenv("GROQ_API_KEY")

class Controller:
    def __init__(self):
        """Initialize controller with ChatGroq LLM"""
        logger.info("🔧 Initializing Controller...")
        
        if not GROQ_KEY:
            logger.error("❌ GROQ_API_KEY not found!")
            raise ValueError("GROQ_API_KEY environment variable not set.")
        
        logger.info(f"🔑 GROQ_API_KEY loaded: {GROQ_KEY[:20]}...")
        
        self.llm = ChatGroq(
            api_key=GROQ_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=512,  # Reduced for faster responses
            timeout=30.0,    # 30 second timeout for routing decisions
            max_retries=2
        )
        
        # logger.info("✅ Controller initialized successfully")

    def decide(self, text, pdf_doc_id=None, prefer_agent=None):
        """Decide which agent to use based on the query"""
        logger.info(f"🎯 Controller.decide() called with text: '{text[:50]}...'")
        logger.info(f"📄 pdf_doc_id: {pdf_doc_id}, prefer_agent: {prefer_agent}")
        
        t = text.lower().strip()

        has_uploaded_pdf = _vectorstore is not None and _vectorstore.index.ntotal > 0

        research_keywords = [
            "arxiv",
            "research paper",
            "research papers",
            "paper on",
            "papers on",
            "latest research",
            "find papers",
            "academic paper",
            "peer reviewed"
        ]
        pdf_keywords = [
            "pdf",
            "document",
            "uploaded file",
            "uploaded pdf",
            "this file",
            "this document",
            "in the document",
            "from the document",
            "summarize",
            "summary"
        ]
        web_keywords = [
            "news",
            "latest",
            "current",
            "today",
            "web",
            "search",
            "internet",
            "out of context",
            "who",
            "what",
            "when",
            "where"
        ]

        # 1) Research-paper intent -> ARXIV
        if any(word in t for word in research_keywords):
            logger.info("✅ Rule matched: ARXIV")
            return "ARXIV", "Rule: research-paper intent detected"

        # 2) PDF-related intent -> PDF_RAG only if PDF context exists
        pdf_intent = any(word in t for word in pdf_keywords)
        if pdf_intent and (pdf_doc_id or has_uploaded_pdf):
            logger.info("✅ Rule matched: PDF_RAG")
            return "PDF_RAG", "Rule: PDF intent with uploaded PDF context"

        # 3) General/out-of-context web intent -> WEB_SEARCH
        if any(word in t for word in web_keywords):
            logger.info("✅ Rule matched: WEB_SEARCH")
            return "WEB_SEARCH", "Rule: general web or out-of-context intent"

        # 4) Optional user override only when no deterministic rule matched
        if prefer_agent:
            reason = f"User requested agent {prefer_agent}"
            decision = prefer_agent.upper()
            logger.info(f"✅ Using preferred agent: {decision}")
            return decision, reason

        # Fallback to LLM for nuanced decision
        logger.info("🤖 No rule matched, falling back to LLM routing...")
        
        prompt = f"""You are an agent router. Choose ONE of: PDF_RAG, WEB_SEARCH, ARXIV.

User query: {text}

Respond with ONLY the agent name (one word):"""

        try:
            logger.info("📡 Calling GROQ LLM...")
            resp = self.llm.invoke(prompt)
            logger.info(f"✅ LLM responded")
            
            # Extract content
            if hasattr(resp, "content"):
                resp_text = resp.content.strip().upper()
            else:
                resp_text = str(resp).strip().upper()
            
            logger.info(f"🎯 LLM decision: {resp_text}")
            
            # Simple extraction - just get the agent name
            if "PDF_RAG" in resp_text:
                decision = "PDF_RAG"
            elif "ARXIV" in resp_text:
                decision = "ARXIV"
            elif "WEB_SEARCH" in resp_text:
                decision = "WEB_SEARCH"
            else:
                decision = "WEB_SEARCH"  # Default fallback
            
            reason = "LLM routing decision"
            
            # Save reasoning
            append_raw_log({
                "input": text,
                "decision": decision,
                "reason": reason,
                "llm_raw": resp_text
            })
            
            logger.info(f"✅ Final decision: {decision}")
            return decision, reason
            
        except Exception as e:
            logger.error(f"❌ LLM call failed: {str(e)}")
            decision = "WEB_SEARCH"
            reason = f"LLM failed, fallback to WEB_SEARCH: {str(e)}"
            logger.info(f"⚠️ Fallback decision: {decision}")
            return decision, reason
