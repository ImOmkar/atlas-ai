from app.embeddings.base import (
    BaseEmbeddingProvider,
)

from app.ai.gemini import client
from app.core.config import settings

class GeminiEmbeddingProvider(
    BaseEmbeddingProvider,
):

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = client.models.embed_content(
            model=settings.gemini_embedding_model,
            contents=text,
        )

        return response.embeddings[0].values