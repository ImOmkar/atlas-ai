from app.embeddings.base import (
    BaseEmbeddingProvider,
)


class GeminiEmbeddingProvider(
    BaseEmbeddingProvider,
):

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return [0.0] * 3072