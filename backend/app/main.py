from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.detections import router as detection_router
from app.api.chat import router as chat_router
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered decision support "
        "for field infrastructure detections."
    ),
    version="0.2.0",
    debug=settings.debug,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    detection_router
)

app.include_router(
    chat_router
)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "status": "running",
        "environment": settings.app_env,
        "version": "0.2.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }