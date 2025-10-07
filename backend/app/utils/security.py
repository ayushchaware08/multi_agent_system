import os
from fastapi import HTTPException, UploadFile

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", 10))  # default 10 MB

def validate_pdf_upload(file: UploadFile):
    """
    Validate uploaded PDF file.
    
    Raises HTTPException if validation fails.
    """

    # 1. Check MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    # 2. Check file size
    file.file.seek(0, os.SEEK_END)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    if size_mb > MAX_UPLOAD_MB:
        raise HTTPException(status_code=400, detail=f"File too large. Max size is {MAX_UPLOAD_MB} MB.")

    # 3. Basic filename safety
    filename = file.filename
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    return True
