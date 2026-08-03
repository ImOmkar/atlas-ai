from abc import (
    ABC,
    abstractmethod,
)

from app.document_chunks.models import (
    DocumentChunk,
)


class BaseReranker(
    ABC,
):

    @abstractmethod
    def rerank(
        self,
        question: str,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        ...