"""
Import all SQLAlchemy models here so they are registered
with Base.metadata before Alembic runs.
"""

from app.auth.models import User

__all__ = ["User"]