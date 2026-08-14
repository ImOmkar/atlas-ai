
from app.reranking.llm import LLMReranker


class RerankingService:

    def __init__(self):

        self.provider = LLMReranker()

    def rerank(
        self,
        question,
        chunks,
    ):

        try:

            return self.provider.rerank(
                question,
                chunks,
            )

        except Exception as e:

            return chunks