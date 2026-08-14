
import json

from app.llm.service import (
    LLMService,
)

from app.rest.models import (
    APIRequest,
)

from app.rest.prompts import (
    REST_GENERATION_PROMPT,
)
from app.utils.llm import parse_llm_json


class RESTGenerator:

    def __init__(self):

        self.llm = LLMService()

    def generate(
        self,
        api_spec: str,
        question: str,
    ):

        prompt = REST_GENERATION_PROMPT.format(
            api=api_spec,
            question=question,
        )

        response = self.llm.generate(
            prompt,
        )

        parsed_response = parse_llm_json(
            response,
        )

        return APIRequest.model_validate(
            parsed_response
        )



# if __name__ == "__main__":
#     generator = RESTGenerator()

#     api_spec = """
#     GET /employees
#     GET /employees/{id}
#     POST /employees
#     """

#     question = "Get the employee with ID 101."

#     api_request = generator.generate(
#         api_spec=api_spec,
#         question=question,
#     )

#     print(api_request)