

from sqlalchemy.orm import Session

from app.document_chunks.repository import (
    DocumentChunkRepository,
)


from app.extraction.prompts import (
    EXTRACTION_PROMPT,
)

import json

from app.llm.service import LLMService


class ExtractionService:

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            DocumentChunkRepository(
                db,
            )
        )

        self.llm = (
            LLMService()
        )


    def extract(
        self,
        document_id: int,
        extraction_schema: dict | None = None,
    ):

        if extraction_schema is None:
            extraction_schema = {}

        schema_json = json.dumps(
            extraction_schema,
            indent=2,
        )

        chunks = (
            self.repository.get_document_chunks(
                document_id,
            )
        )

        document = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        prompt = EXTRACTION_PROMPT.format(
            extraction_schema=schema_json,
            document=document,
        )

        result = self.llm.generate(
            prompt,
        )

        return result


