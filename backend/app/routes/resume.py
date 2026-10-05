from fastapi import APIRouter, UploadFile, HTTPException

router  = APIRouter()

@router.post("/api/resume/upload")
async def resume_upload(file: UploadFile):
   if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
         raise HTTPException(
        status_code=400,
        detail="Unsupported file type"
    )   
   return {"filename": file.filename,
            "content_type": file.content_type}