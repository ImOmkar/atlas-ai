import json


from app.agents.prompts import (
    TOOL_ARGUMENT_PROMPT,
)
from app.llm.service import LLMService

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

        return json.loads(
            response,
        )