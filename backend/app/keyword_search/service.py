from sqlalchemy.orm import Session

from app.keyword_search.repository import (
    KeywordSearchRepository,
)

from app.keyword_search.providers.ilike import (
    ILikeProvider,
)


from app.keyword_search.providers.bm25 import (
    BM25Provider,
)


class KeywordSearchService:

    def __init__(
        self,
        db: Session,
    ):

       self.provider = (
            BM25Provider(
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

        return self.provider.search(
            organization_id,
            project_id,
            query,
            limit,
        )



