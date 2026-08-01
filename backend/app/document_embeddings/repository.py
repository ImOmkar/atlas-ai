from sqlalchemy.orm import Session

from app.document_embeddings.models import (
    DocumentEmbedding,
)


class DocumentEmbeddingRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create_many(
        self,
        embeddings: list[DocumentEmbedding],
    ):

        self.db.add_all(
            embeddings,
        )

        self.db.commit()