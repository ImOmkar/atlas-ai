from sqlalchemy import text

from sqlalchemy.orm import Session


class SQLRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def execute(
        self,
        query: str,
    ):

        result = self.db.execute(
            text(query),
        )

        return result.fetchall()