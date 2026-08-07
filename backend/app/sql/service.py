

from sqlalchemy.orm import Session

from app.sql.repository import (
    SQLRepository,
)


class SQLService:

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            SQLRepository(
                db,
            )
        )

    def execute(
        self,
        query: str,
    ):

        return self.repository.execute(
            query,
        )