from app.keyword_search.base import (
    BaseKeywordSearchProvider,
)


from sqlalchemy.orm import Session

import bm25s

from app.keyword_search.base import (
    BaseKeywordSearchProvider,
)

from app.keyword_search.repository import (
    KeywordSearchRepository,
)


class BM25Provider(
    BaseKeywordSearchProvider,
):

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            KeywordSearchRepository(
                db,
            )
        )

    def search(
        self,
        organization_id: int,
        project_id: int,
        query: str,
        limit: int = 10,
    ):

        chunks = self.repository.get_chunks(
            organization_id,
            project_id,
        )

        if not chunks:
            return []


        corpus = [
            chunk.content
            for chunk, _ in chunks
        ]

        corpus_tokens = bm25s.tokenize(
            corpus,
        )

        retriever = bm25s.BM25()

        retriever.index(
            corpus_tokens,
        )

        query_tokens = bm25s.tokenize(
            [query],
        )

        results, scores = retriever.retrieve(
            query_tokens,
            k=limit,
        )

        retrieved_chunks = []

        for index in results[0]:

            chunk, document = chunks[index]

            retrieved_chunks.append(
                (
                    chunk,
                    document,
                    1.0,
                )
            )

        return retrieved_chunks
