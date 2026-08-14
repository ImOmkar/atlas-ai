from fastapi import FastAPI
from app.core.config import settings

from sqlalchemy import text

from app.db.engine import engine

from app.core.exception_handlers import register_exception_handlers

from app.auth.router import router as auth_router
from app.organizations.router import router as organization_router
from app.projects.router import router as project_router
from app.documents.router import router as document_router
from app.chat.router import router as chat_router
from app.conversation.router import router as conversation_router
from app.rfps.router import router as rfp_router
from app.rfp_requirements.router import (
    router as rfp_requirements_router,
)
from app.proposals.router import router as proposal_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(organization_router)
app.include_router(project_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(rfp_router)
app.include_router(rfp_requirements_router)
app.include_router(proposal_router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }

@app.get("/db-check")
def db_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()

    return {
        "status": "connected",
        "database": version,
    }