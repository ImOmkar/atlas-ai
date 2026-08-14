


from sqlalchemy.orm import Session

from app.document_chunks.repository import (
    DocumentChunkRepository,
)

from app.summarization.prompts import (
    SUMMARY_PROMPT,
)
from app.llm.service import LLMService


class SummarizationService:

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

    def summarize(
        self,
        document_id: int,
    ):
        chunks = (
            self.repository.get_document_chunks(
                document_id,
            )
        )

        document = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        prompt = SUMMARY_PROMPT.format(
            document=document,
        )
        summary = self.llm.generate(
            prompt,
        )

        return summary