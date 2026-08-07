

from app.tools.base import (
    BaseTool,
)

from app.rest.registry import (
    RESTRegistry,
)

from app.rest.service import (
    RESTQueryService,
)


class RESTTool(
    BaseTool,
):

    def __init__(
        self,
    ):

        self.registry = (
            RESTRegistry()
        )

        self.service = (
            RESTQueryService()
        )

    def name(
        self,
    ):

        return "rest"

    def description(
        self,
    ):

        return (
            "Execute REST API requests."
        )

    def execute(
        self,
        arguments: dict,
    ):

        system = arguments["system"]

        question = arguments["question"]

        config = self.registry.get(
            system,
        )

        return self.service.execute(
            api_spec=config["api_spec"],
            base_url=config["base_url"],
            headers=config["headers"],
            question=question,
        )




# if __name__ == "__main__":

#     tool = RESTTool()

#     result = tool.execute(
#         {
#             "system": "jsonplaceholder",
#             "question": "Get user 1.",
#         }
#     )

#     print(result)