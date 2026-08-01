"""
Import all SQLAlchemy models here so they are registered
with Base.metadata before Alembic runs.
"""

from app.auth.models import RefreshToken, User
from app.organizations.models import Organization, OrganizationMember
from app.projects.models import Project
from app.documents.models import Document
from app.document_chunks.models import DocumentChunk
from app.document_embeddings.models import (
    DocumentEmbedding,
)

__all__ = [
    "User",
    "RefreshToken",
    "Organization",
    "OrganizationMember",
    "Project",
    "Document",
    "DocumentChunk",
    "DocumentEmbedding"
]