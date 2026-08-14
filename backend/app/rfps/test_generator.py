
from app.db.session import SessionLocal

from app.document_chunks.repository import (
    DocumentChunkRepository,
)

from app.rfps.generator import (
    RFPGenerator,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            DocumentChunkRepository(
                db,
            )
        )

        chunks = (
            repository.get_document_chunks(
                20,
            )
        )

        document = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        print(
            f"Loaded {len(chunks)} chunks."
        )

        generator = (
            RFPGenerator()
        )

        print("\nDOCUMENT PREVIEW:")
        print(document[:10000])

        result = generator.generate(
            document,
        )

        print(
            "\nRFP EXTRACTION RESULT:"
        )

        print(
            result
        )

    finally:

        db.close()