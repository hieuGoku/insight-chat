"""API routes for the app."""

from fastapi import APIRouter

from app.api.routes import (
    health_router,
    ingest_router,
    user_router,
    session_router,
    message_router,
    auth_router,
    chat_router,
)

api_router = APIRouter()

api_router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(ingest_router.router, prefix="/ingest", tags=["Ingest"])
api_router.include_router(user_router.router, prefix="/user", tags=["User"])
api_router.include_router(session_router.router, prefix="/session", tags=["Chat Session"])
api_router.include_router(message_router.router, prefix="/message", tags=["Message"])
api_router.include_router(chat_router.router, prefix="/chat", tags=["Chat"])
api_router.include_router(health_router.router, prefix="/health", tags=["Health"])
