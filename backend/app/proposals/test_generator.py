
from app.db.session import SessionLocal

from app.document_chunks.repository import (
    DocumentChunkRepository,
)

from app.proposals.generator import (
    ProposalGenerator,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        document_id = 23  # CHANGE THIS

        repository = (
            DocumentChunkRepository(db)
        )

        chunks = repository.get_document_chunks(
            document_id,
        )

        print(
            f"Loaded {len(chunks)} chunks."
        )

        document = "\n".join(
            chunk.content
            for chunk in chunks
        )

        print(
            "\nDOCUMENT PREVIEW:"
        )

        print(
            document
        )

        generator = ProposalGenerator()

        result = generator.generate(
            document,
        )

        print(
            "\nPROPOSAL EXTRACTION RESULT:"
        )

        print(
            result
        )

    finally:

        db.close()