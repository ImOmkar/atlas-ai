



from app.reranking.base import BaseReranker
from app.llm.service import LLMService
from app.document_chunks.models import DocumentChunk


class LLMReranker(BaseReranker):

    def __init__(self):

        self.llm = LLMService()

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
        You are Atlas AI's document reranker.

        Given a user's question and a list of retrieved document chunks,
        rank the chunks from MOST relevant to LEAST relevant.

        Return ONLY the chunk indices.

        Rules:

        - Return one integer per line.
        - Do not explain.
        - Do not use markdown.
        - Do not include bullets.
        - Do not include commas.
        - Do not include words.

        Example:

        4
        2
        0
        3

        Question:

        {question}

        Chunks:

        {''.join(numbered_chunks)}
        """

        response = self.llm.generate(
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

        if not indices:

            return chunks

        reranked = []

        used = set()

        for index in indices:

            if 0 <= index < len(chunks):

                reranked.append(
                    chunks[index]
                )

                used.add(index)

        for index, chunk in enumerate(chunks):

            if index not in used:

                reranked.append(chunk)

        return reranked
