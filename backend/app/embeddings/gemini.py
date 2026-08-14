from google import genai

from app.core.config import settings

from app.embeddings.base import (
    BaseEmbeddingProvider,
)


class GeminiEmbeddingProvider(
    BaseEmbeddingProvider,
):

    def __init__(
        self,
    ):

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = (
            settings.gemini_embedding_model
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values