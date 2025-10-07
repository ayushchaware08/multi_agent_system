
from fastapi import APIRouter
from pydantic import BaseModel
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
def ask(req: AskRequest):
    controller = Controller()
    decision, rationale = controller.decide(req.text, pdf_doc_id=req.pdf_doc_id, prefer_agent=req.prefer_agent)

    # route
    result = {}
    if decision == "PDF_RAG":
        answer, trace = run_pdf_rag_query(req.text, doc_id=req.pdf_doc_id)
    elif decision == "WEB_SEARCH":
        answer, trace = run_web_search(req.text)
    elif decision == "ARXIV":
        answer, trace = run_arxiv_query(req.text)
    else:
        answer, trace = "No agent chosen", {}

    # record decision & trace
    log_entry = {
        "timestamp": record_decision(decision, rationale, req.text, trace)
    }

    return {"answer": answer, "agents_used": decision, "rationale": rationale, "trace": trace}
