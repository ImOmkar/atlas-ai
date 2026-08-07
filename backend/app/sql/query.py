from sqlalchemy.orm import Session

from app.sql.generator import (
    SQLGenerator,
)

from app.sql.validator import (
    SQLValidator,
)

from app.sql.service import (
    SQLService,
)
from app.sql.reasoner import SQLReasoner


class SQLQueryService:

    def __init__(
        self,
        db: Session,
    ):

        self.generator = (
            SQLGenerator()
        )

        self.validator = (
            SQLValidator()
        )

        self.service = (
            SQLService(
                db,
            )
        )

        self.reasoner = SQLReasoner()

    def execute(
        self,
        question: str,
    ):

        query = self.generator.generate(
            question,
        )

        self.validator.validate(
            query,
        )

        rows = self.service.execute(
            query,
        )

        return self.reasoner.answer(
            question,
            rows,
        )




# if __name__ == "__main__":
#     from app.db.session import (
#         SessionLocal,
#     )

#     db = SessionLocal()

#     try:

#         service = SQLQueryService(
#             db,
#         )

#         rows = service.execute(
#             "Show current database time."
#         )

#         print(
#             rows
#         )

#     finally:

#         db.close()