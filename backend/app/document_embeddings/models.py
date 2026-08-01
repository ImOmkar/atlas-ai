from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.db.mixins import TimestampMixin


class DocumentEmbedding(
    TimestampMixin,
    Base,
):
    __tablename__ = "document_embeddings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey(
            "document_chunks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
    )