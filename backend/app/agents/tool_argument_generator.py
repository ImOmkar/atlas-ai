import json


from app.agents.prompts import (
    TOOL_ARGUMENT_PROMPT,
)
from app.llm.service import LLMService
from app.utils.llm import parse_llm_json

class ToolArgumentGenerator:

    def __init__(self):
    
            self.llm = (
                LLMService()
            )

            
    def generate(
        self,
        tool: str,
        question: str,
    ):
        prompt = TOOL_ARGUMENT_PROMPT.format(
            tool=tool,
            question=question,
        )

        response = self.llm.generate(
            prompt,
        )

        parsed_response = parse_llm_json(
            response,
        )

        return parsed_response


# if __name__ == "__main__":

#     generator = ToolArgumentGenerator()

#     test = generator.generate(
#         "rest",
#         ""
#     )

#     print(test)