from fastapi import FastAPI
from app.config import settings
from app.routers import questions_router, answers_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Ручки
app.include_router(questions_router, prefix=settings.API_V1_STR)
app.include_router(answers_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to PyQueswers API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
