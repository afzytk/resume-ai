from fastapi import APIRouter, UploadFile, HTTPException, Form
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ats_analyzer import analyze_resume

router  = APIRouter()

@router.post("/api/resume/upload")
async def resume_upload(file: UploadFile, job_role:str = Form(...)):
   if file.content_type != "application/pdf":
         raise HTTPException(
        status_code=400,
        detail="Unsupported file type"
    )   
   contents = await file.read()
   text = extract_text_from_pdf(contents)
   analysis = analyze_resume(
    text,
    job_role
)
   return {"filename": file.filename,
            "job role": job_role,
            "analysis": analysis}