import json

from app.ai.gemini import (
    generate_tool_arguments,
)

from app.agents.prompts import (
    TOOL_ARGUMENT_PROMPT,
)

class ToolArgumentGenerator:
    def generate(
        self,
        tool: str,
        question: str,
    ):
        prompt = TOOL_ARGUMENT_PROMPT.format(
            tool=tool,
            question=question,
        )

        response = generate_tool_arguments(
            prompt,
        )

        return json.loads(
            response,
        )