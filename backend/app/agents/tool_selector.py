
from app.agents.prompts import (
    TOOL_SELECTION_PROMPT,
)

from app.agents.enums import (
    ToolDecision,
)
from app.llm.service import LLMService

class ToolSelector:

    def __init__(self):

        self.llm = LLMService()
    
    def choose(
        self,
        user_input: str,
    ):
        prompt = TOOL_SELECTION_PROMPT.format(
            user_input=user_input,
        )

        tool = self.llm.generate(
            prompt,
        ).strip()

        return ToolDecision(
            tool.lower(),
        )