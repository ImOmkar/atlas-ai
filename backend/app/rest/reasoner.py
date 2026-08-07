

from app.llm.service import (
    LLMService,
)

from app.rest.prompts import (
    REST_REASONING_PROMPT,
)


class RESTReasoner:

    def __init__(
        self,
    ):

        self.llm = (
            LLMService()
        )

    def answer(
        self,
        question: str,
        response,
    ):

        prompt = REST_REASONING_PROMPT.format(
            question=question,
            response=response,
        )

        return self.llm.generate(
            prompt,
        )


    

# if __name__ == "__main__":

#     response = {
#         "id": 101,
#         "name": "John Doe",
#         "department": "Engineering",
#     }

#     reasoner = RESTReasoner()

#     answer = reasoner.answer(
#         "Get employee details.",
#         response,
#     )

#     print(answer)