
from app.tools.base import (
    BaseTool,
)


class CalculatorTool(
    BaseTool,
):

    def name(
        self,
    ):

        return "calculator"

    def description(
        self,
    ):

        return (
            "Perform mathematical calculations."
        )

    def execute(
        self,
        arguments: dict,
    ):

        expression = arguments["expression"]

        return eval(
            expression,
        )