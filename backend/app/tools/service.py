
from app.tools.registry import (
    ToolRegistry,
)


class ToolService:

    def __init__(
        self,
    ):

        self.registry = (
            ToolRegistry()
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
#     service = (
#         ToolService()
#     )

#     result = service.execute(
#         "calculator",
#         {
#             "expression": "25 * 18 + 100",
#         },
#     )

#     print(
#         result,
#     )