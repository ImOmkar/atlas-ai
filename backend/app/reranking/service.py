from app.document_chunks.models import (
    DocumentChunk,
)

from app.reranking.providers.gemini import (
    GeminiReranker,
)


class RerankingService:

    def __init__(self):

        self.provider = (
            GeminiReranker()
        )

    def rerank(
        self,
        question: str,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        return self.provider.rerank(
            question,
            chunks,
        )