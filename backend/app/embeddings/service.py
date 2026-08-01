from app.embeddings import (
    EMBEDDING_PROVIDER,
)


class EmbeddingService:

    def __init__(self):
        self.provider = EMBEDDING_PROVIDER

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed(
            text,
        )