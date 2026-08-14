
from sqlalchemy.orm import Session

from app.keyword_search.base import (
    BaseKeywordSearchProvider,
)

from app.keyword_search.repository import (
    KeywordSearchRepository,
)


class ILikeProvider(
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

        return self.repository.search(
            organization_id,
            project_id,
            query,
            limit,
        )
