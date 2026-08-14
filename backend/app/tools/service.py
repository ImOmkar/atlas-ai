from sqlalchemy.orm import Session
from app.tools.registry import (
    ToolRegistry,
)

from app.db.session import (
    SessionLocal,
)


class ToolService:

    def __init__(
        self,
        db: Session,
    ):

        self.registry = (
            ToolRegistry(db)
        )


    def execute(
        self,
        tool_name: str,
        arguments: dict,
    ):

        tool = self.registry.get(
            tool_name,
        )

        if tool is None:

            raise ValueError(
                "Unknown tool."
            )

        return tool.execute(
            arguments,
        )



# if __name__ == "__main__":

#     db = SessionLocal()

#     try:

#         service = ToolService(
#             db,
#         )

#         result = service.execute(
#             "sql",
#             {
#                 "query": "SELECT COUNT(*) FROM documents;"
#             },
#         )

#         print(result)

#     finally:

#         db.close()