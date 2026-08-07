

from app.rest.generator import (
    RESTGenerator,
)

from app.rest.validator import (
    RESTValidator,
)

from app.rest.repository import (
    RESTRepository,
)

from app.rest.reasoner import (
    RESTReasoner,
)


class RESTQueryService:

    def __init__(
        self,
    ):

        self.generator = (
            RESTGenerator()
        )

        self.validator = (
            RESTValidator()
        )

        self.repository = (
            RESTRepository()
        )

        self.reasoner = (
            RESTReasoner()
        )

    def execute(
        self,
        api_spec: str,
        base_url: str,
        question: str,
        headers: dict | None = None,
    ):

        request = self.generator.generate(
            api_spec,
            question,
        )

        self.validator.validate(
            request,
        )

        response = self.repository.execute(
            base_url,
            request,
            headers,
        )

        return self.reasoner.answer(
            question,
            response,
        )




# if __name__ == "__main__":

#     api_spec = """
#     GET /users
#     GET /users/{id}
#     """

#     service = RESTQueryService()

#     answer = service.execute(
#         api_spec=api_spec,
#         base_url="https://jsonplaceholder.typicode.com",
#         question="Get user 1.",
#     )

#     print(answer)