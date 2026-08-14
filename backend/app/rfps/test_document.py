from app.db.session import SessionLocal

from app.document_chunks.repository import (
    DocumentChunkRepository,
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

        print(
            f"Total chunks: {len(chunks)}"
        )

        for chunk in chunks:

            print(
                "\n"
                + "=" * 80
            )

            print(
                f"CHUNK {chunk.chunk_index}"
            )

            print(
                "=" * 80
            )

            print(
                chunk.content[:2000]
            )

    finally:

        db.close()