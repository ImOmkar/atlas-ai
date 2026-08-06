
from app.tools.calculator import (
    CalculatorTool,
)

class ToolRegistry:

    def __init__(
        self,
    ):

        self.tools = {
            "calculator": CalculatorTool(),
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


    