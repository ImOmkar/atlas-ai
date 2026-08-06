from sqlalchemy.orm import Session

from app.document_chunks.models import (
    DocumentChunk,
)


class DocumentChunkRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create_many(
        self,
        chunks: list[DocumentChunk],
    ):

        self.db.add_all(
            chunks,
        )

        self.db.commit()

    def get_document_chunks(
        self,
        document_id: int,
    ):
        return (
            self.db.query(
                DocumentChunk,
            )
            .filter(
                DocumentChunk.document_id == document_id,
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .all()
        )