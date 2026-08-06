
from app.ai.gemini import (
    choose_tool,
)

from app.agents.prompts import (
    TOOL_SELECTION_PROMPT,
)

from app.agents.enums import (
    ToolDecision,
)

class ToolSelector:
    def choose(
        self,
        user_input: str,
    ):
        prompt = TOOL_SELECTION_PROMPT.format(
            user_input=user_input,
        )

        tool = choose_tool(
            prompt,
        )

        return ToolDecision(
            tool.lower(),
        )