from sqlalchemy.orm import Session

from app.document_embeddings.models import (
    DocumentEmbedding,
)



from app.document_embeddings.models import (
    DocumentEmbedding,
)

from app.document_chunks.models import (
    DocumentChunk,
)

from app.documents.models import Document
from app.projects.models import Project


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

    def semantic_search(
        self,
        organization_id: int,
        project_id: int,
        embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:

        distance = DocumentEmbedding.embedding.cosine_distance(
            embedding,
        )

        return (
            self.db.query(DocumentChunk, Document, distance.label("distance"),)
            .join(
                DocumentEmbedding,
                DocumentEmbedding.chunk_id == DocumentChunk.id,
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .join(
                Project,
                Project.id == Document.project_id,
            )
            .filter(
                Project.id == project_id,
                Project.organization_id == organization_id,
            )
            .order_by(
                DocumentEmbedding.embedding.cosine_distance(
                    embedding,
                )
            )
            .limit(limit)
            .all()
        )