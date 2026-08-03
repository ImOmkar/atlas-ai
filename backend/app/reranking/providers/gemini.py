from app.reranking.base import (
    BaseReranker,
)

from app.document_chunks.models import (
    DocumentChunk,
)
from app.ai.gemini import rerank_chunks


class GeminiReranker(
    BaseReranker,
):

    def rerank(
        self,
        question: str,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        numbered_chunks = []

        for index, (chunk, document, distance) in enumerate(chunks):

            numbered_chunks.append(
                f"""
        [{index}]

        {chunk.content}
        """
            )

        prompt = f"""
            You are a document reranking assistant.

            Given the user's question and the retrieved document chunks,

            rank the chunks from MOST relevant to LEAST relevant.

            Return ONLY the chunk numbers.

            Question:

            {question}

            Chunks:

            {''.join(numbered_chunks)}
        """

        response = rerank_chunks(
            prompt,
        )

        print(response)

        indices = []

        for line in response.splitlines():

            line = line.strip()

            if line.isdigit():

                indices.append(
                    int(line)
                )

        reranked = []

        for index in indices:

            if 0 <= index < len(chunks):

                reranked.append(
                    chunks[index]
                )

        return reranked
