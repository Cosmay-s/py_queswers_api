from fastapi import FastAPI
from app.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)


@app.get("/")
async def root():
    return {"message": "PyQueswers API is run"}


@app.get("/")
async def health_check():
    return {"status": "healthy"}
