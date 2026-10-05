from fastapi import APIRouter, UploadFile, HTTPException
from app.services.pdf_parser import extract_text_from_pdf

router  = APIRouter()

@router.post("/api/resume/upload")
async def resume_upload(file: UploadFile):
   if file.content_type not in "application/pdf":
         raise HTTPException(
        status_code=400,
        detail="Unsupported file type"
    )   
   contents = await file.read()
   text = extract_text_from_pdf(contents)
   return {"filename": file.filename,
            "content_type": file.content_type,
            "text":text}