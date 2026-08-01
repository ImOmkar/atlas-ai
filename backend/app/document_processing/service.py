from sqlalchemy.orm import Session

from app.documents.models import Document

from pathlib import Path

from app.documents.enums import DocumentStatus
from app.documents.repository import DocumentRepository

from app.document_processing.extractors import (
    EXTRACTORS,
)

import traceback

from app.document_processing.ocr import OCR_ENGINE

from app.document_processing.chunking import (
    CHUNKER,
)

from app.document_chunks.models import (
    DocumentChunk,
)

from app.document_chunks.repository import (
    DocumentChunkRepository,
)


from app.embeddings.service import (
    EmbeddingService,
)

from app.document_embeddings.models import (
    DocumentEmbedding,
)

from app.document_embeddings.repository import (
    DocumentEmbeddingRepository,
)

class DocumentProcessingService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.document_repository = DocumentRepository(db)
        self.chunk_repository = (
                                    DocumentChunkRepository(db)
                                )

        self.embedding_service = EmbeddingService()

        self.embedding_repository = (
            DocumentEmbeddingRepository(db)
        )

    def process_document(
        self,
        document_id: int,
    ):
        document = self.document_repository.get_by_id_(
            document_id,
        )

        if document is None:
            return

        path = Path(document.storage_path)

        extension = path.suffix.lower()

        extractor = EXTRACTORS.get(
            extension,
        )

        if extractor is None:
            document.status = DocumentStatus.FAILED

            self.document_repository.update(
                document,
            )

            return

        try:
            text = extractor.extract(path)

            if not text.strip():
                text = OCR_ENGINE.extract(path)


            chunks = CHUNKER.chunk(
                text,
            )

            db_chunks = []

            for index, chunk in enumerate(chunks):

                db_chunks.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=chunk,
                    )
                )

            self.chunk_repository.create_many(
                db_chunks,
            )

            db_embeddings = []

            for chunk in db_chunks:

                vector = self.embedding_service.embed(
                    chunk.content,
                )

                db_embeddings.append(
                    DocumentEmbedding(
                        chunk_id=chunk.id,
                        provider="gemini",
                        model="placeholder",
                        embedding=vector,
                    )
                )

            self.embedding_repository.create_many(
                db_embeddings,
            )
            
            document.extracted_text = text

            document.status = DocumentStatus.READY

        except Exception as e:
            traceback.print_exc()
            print(e)

            document.status = DocumentStatus.FAILED

        self.document_repository.update(
            document,
        )