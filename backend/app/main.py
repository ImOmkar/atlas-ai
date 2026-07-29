from fastapi import FastAPI
from app.core.config import settings

from sqlalchemy import text

from app.db.engine import engine

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

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