from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
import os
import shutil
import time
import logging
from app.utils.security import validate_pdf_upload
from app.agents.pdf_rag import ingest_pdf_to_chroma

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory status tracking
upload_status = {}

@router.post("/", status_code=202)  # 202 Accepted (processing in background)
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Upload PDF and process in background.
    Returns immediately with doc_id for status tracking.
    """
    try:
        logger.info(f"📤 Received upload: {file.filename}")
        
        # 1) Validation (size & mimetype)
        validate_pdf_upload(file)  # raises HTTPException if invalid
        
        # 2) Save uploaded file with unique doc_id
        ts = int(time.time())
        doc_id = f"upload_{ts}"
        dest_path = os.path.join(UPLOAD_DIR, f"{ts}_{file.filename}")
        
        # Save file
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        logger.info(f"✅ File saved: {dest_path}")
        
        # Get file size
        file_size = os.path.getsize(dest_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Initialize status
        upload_status[doc_id] = {
            "status": "processing",
            "message": "PDF uploaded, creating embeddings...",
            "filename": file.filename,
            "file_size_mb": file_size_mb,
            "uploaded_at": time.time(),
            "doc_id": doc_id
        }
        
        # 3) Process PDF in background task
        background_tasks.add_task(
            process_pdf_background,
            dest_path,
            doc_id,
            file.filename
        )
        
        logger.info(f"🚀 Background processing started for doc_id: {doc_id}")
        
        return {
            "status": "accepted",
            "doc_id": doc_id,
            "filename": file.filename,
            "file_size_mb": file_size_mb,
            "message": "PDF uploaded successfully. Processing embeddings in background.",
            "check_status": f"/upload/status/{doc_id}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def process_pdf_background(pdf_path: str, doc_id: str, filename: str):
    """
    Background task to ingest PDF into ChromaDB
    """
    try:
        logger.info(f"🔄 Starting PDF ingestion for {doc_id}")
        
        # Update status
        upload_status[doc_id]["status"] = "embedding"
        upload_status[doc_id]["message"] = "Creating vector embeddings..."
        
        # Ingest PDF into Chroma
        ingest_result = ingest_pdf_to_chroma(pdf_path, doc_id)
        
        if ingest_result["status"] == "success":
            # Success
            upload_status[doc_id] = {
                "status": "completed",
                "message": ingest_result["message"],
                "filename": filename,
                "doc_id": doc_id,
                "chunks_count": ingest_result.get("chunks_count", 0),
                "completed_at": time.time()
            }
            logger.info(f"✅ PDF ingestion completed for {doc_id}: {ingest_result['chunks_count']} chunks")
        else:
            # Ingestion failed
            upload_status[doc_id] = {
                "status": "failed",
                "message": ingest_result["message"],
                "filename": filename,
                "doc_id": doc_id,
                "failed_at": time.time()
            }
            logger.error(f"❌ PDF ingestion failed for {doc_id}: {ingest_result['message']}")
            
            # Clean up file on failure
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                logger.info(f"🗑️ Cleaned up file: {pdf_path}")
                
    except Exception as e:
        logger.error(f"❌ Background processing error for {doc_id}: {str(e)}")
        upload_status[doc_id] = {
            "status": "failed",
            "message": f"Processing failed: {str(e)}",
            "filename": filename,
            "doc_id": doc_id,
            "failed_at": time.time()
        }
        
        # Clean up file on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@router.get("/status/{doc_id}")
async def get_upload_status(doc_id: str):
    """
    Check processing status of uploaded PDF
    """
    if doc_id not in upload_status:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    
    return upload_status[doc_id]

@router.get("/list")
async def list_uploads():
    """
    List all uploaded documents and their status
    """
    return {
        "total": len(upload_status),
        "documents": list(upload_status.values())
    }

@router.delete("/{doc_id}")
async def delete_upload(doc_id: str):
    """
    Delete uploaded document and remove from status
    """
    if doc_id not in upload_status:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    
    # Remove from status
    doc_info = upload_status.pop(doc_id)
    
    logger.info(f"🗑️ Deleted document: {doc_id}")
    
    return {
        "status": "deleted",
        "doc_id": doc_id,
        "filename": doc_info.get("filename")
    }
@router.delete("/clear-failed")
async def clear_failed_uploads():
    """Clear all failed upload statuses"""
    failed_docs = [
        doc_id for doc_id, status in upload_status.items()
        if status.get("status") in ["failed", "error"]
    ]
    
    for doc_id in failed_docs:
        upload_status.pop(doc_id)
    
    logger.info(f"🗑️ Cleared {len(failed_docs)} failed uploads")
    
    return {
        "cleared": len(failed_docs),
        "cleared_doc_ids": failed_docs
    }
