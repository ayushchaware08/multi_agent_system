from fastapi import APIRouter, File, UploadFile, HTTPException
import os, shutil, time
from app.utils.security import validate_pdf_upload
from app.agents.pdf_rag import ingest_pdf_to_chroma

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", status_code=201)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF and ingest into vector database"""
    
    # 1) Validation (size & mimetype)
    validate_pdf_upload(file)  # raises HTTPException if invalid

    # 2) Save uploaded file with unique doc_id
    ts = int(time.time())
    doc_id = f"upload_{ts}"
    dest_path = os.path.join(UPLOAD_DIR, f"{ts}_{file.filename}")
    
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 3) Ingest PDF into Chroma using pdf_rag function
    ingest_result = ingest_pdf_to_chroma(dest_path, doc_id)
    
    if ingest_result["status"] == "error":
        # Clean up file if ingestion failed
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise HTTPException(status_code=500, detail=ingest_result["message"])

    return {
        "status": "success",
        "doc_id": doc_id,
        "filename": file.filename,
        "message": f"PDF uploaded and ingested successfully. {ingest_result['chunks_count']} chunks created.",
        "ingestion_details": ingest_result
    }
