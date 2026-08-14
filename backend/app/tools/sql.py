from sqlalchemy.orm import Session

from app.tools.base import (
    BaseTool,
)

from app.sql.service import (
    SQLService,
)
from app.sql.query import SQLQueryService


class SQLTool(
    BaseTool,
):
    def __init__(
        self,
        db: Session,
    ):

        self.service = (
            SQLQueryService(
                db,
            )
        )


    def name(
        self,
    ):

        return "sql"

    def description(
        self,
    ):

        return (
            "Query the application's PostgreSQL database using read-only SELECT statements."
        )

    def execute(
        self,
        arguments: dict,
    ):

        print(arguments)

        return self.service.execute(
            arguments["question"],
        )


    