from sqlalchemy.orm import Session
from app.tools.calculator import (
    CalculatorTool,
)
from app.tools.sql import SQLTool
from app.tools.rest import (
    RESTTool,
)

class ToolRegistry:

    def __init__(
        self,
        db: Session,
    ):

        self.tools = {
            "calculator": CalculatorTool(),
            "sql": SQLTool(db),
            "rest": RESTTool()
        }

    def get(
        self,
        name: str,
    ):

        return self.tools.get(
            name,
        )


    def list_tools(
        self,
    ):

        return list(
            self.tools.values()
        )


