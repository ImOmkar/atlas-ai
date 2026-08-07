
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
            "Evaluate arithmetic expressions and perform mathematical calculations."
        )

    def execute(
        self,
        arguments: dict,
    ):

        expression = arguments["expression"]

        return eval(
            expression,
        )