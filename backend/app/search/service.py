from sqlalchemy.orm import Session

from app.embeddings.service import (
    EmbeddingService,
)

from app.document_embeddings.repository import (
    DocumentEmbeddingRepository,
)

from app.reranking.service import (
    RerankingService,
)

from app.keyword_search.service import (
    KeywordSearchService,
)

class SearchService:

    def __init__(
        self,
        db: Session,
    ):

        self.embedding_service = (
            EmbeddingService()
        )

        self.repository = (
            DocumentEmbeddingRepository(db)
        )

        self.reranker = (
            RerankingService()
        )

        self.keyword_search = (
            KeywordSearchService(
                db,
            )
        )

    def search(
        self,
        organization_id: int,
        project_id: int,
        query: str,
        limit: int = 5,
    ):

        query_embedding = (
            self.embedding_service.embed(
                query,
            )
        )

        vector_chunks = self.repository.semantic_search(
            organization_id,
            project_id,
            query_embedding,
            limit,
        )

        keyword_chunks = (
            self.keyword_search.search(
                organization_id,
                project_id,
                query,
                limit,
            )
        )

        keyword_chunks = (
            self.keyword_search.search(
                organization_id,
                project_id,
                query,
                limit,
            )
        )

        chunks = (
            vector_chunks +
            keyword_chunks
        )

        unique = {}

        for chunk, document, distance in chunks:

            if chunk.id not in unique:

                unique[chunk.id] = (
                    chunk,
                    document,
                    distance,
                )

        chunks = list(
            unique.values()
        )

        print("Vector:", len(vector_chunks))
        print("Keyword:", len(keyword_chunks))
        print("Merged:", len(chunks))

        chunks = self.reranker.rerank(
            query,
            chunks,
        )

        print("After rerank:", len(chunks))

        return chunks