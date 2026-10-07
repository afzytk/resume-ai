from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.resume import router as resume_router


app = FastAPI()
app.include_router(health_router)
app.include_router(resume_router)

@app.get("/")
def  read_root():
    return {"Hello":"World"}