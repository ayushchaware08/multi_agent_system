from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from app.agents.controller import Controller
from app.agents.pdf_rag import run_pdf_rag_query
from app.agents.web_search import run_web_search
from app.agents.arxiv_agent import run_arxiv_query
from app.utils.logging_utils import record_decision


router = APIRouter()


class AskRequest(BaseModel):
    text: str
    pdf_doc_id: str = None   # optional: reference to uploaded PDF
    prefer_agent: str = None


@router.post("/")
async def ask(req: AskRequest):
    """
    Main endpoint to process user queries through the multi-agent system.
    Uses async/await to prevent blocking and includes proper error handling.
    """
    try:
        # Initialize controller
        controller = Controller()
        
        # Run decision logic in thread pool to avoid blocking
        decision, rationale = await asyncio.to_thread(
            controller.decide,
            req.text,
            pdf_doc_id=req.pdf_doc_id,
            prefer_agent=req.prefer_agent
        )
        
        # Route to appropriate agent based on decision
        if decision == "PDF_RAG":
            answer, trace = await asyncio.to_thread(
                run_pdf_rag_query, 
                req.text, 
                doc_id=req.pdf_doc_id
            )
        elif decision == "WEB_SEARCH":
            answer, trace = await asyncio.to_thread(
                run_web_search, 
                req.text
            )
        elif decision == "ARXIV":
            answer, trace = await asyncio.to_thread(
                run_arxiv_query, 
                req.text
            )
        else:
            answer = "No agent chosen"
            trace = {}
        
        # Record decision & trace for logging/analytics
        log_entry = {
            "timestamp": record_decision(decision, rationale, req.text, trace)
        }
        
        # Return structured response
        return {
            "answer": answer, 
            "agents_used": decision, 
            "rationale": rationale, 
            "trace": trace
        }
        
    except Exception as e:
        # Proper error handling with HTTP status codes
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )
