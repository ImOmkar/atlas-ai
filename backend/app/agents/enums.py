from enum import Enum


class AgentTask(
    Enum,
):

    CHAT = "chat"

    SUMMARIZE = "summarize"

    EXTRACT = "extract"

    COMPARE = "compare"


class ToolDecision(
    Enum,
):

    NONE = "none"

    CALCULATOR = "calculator"