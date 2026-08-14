
from app.llm.service import (
    LLMService,
)

from app.sql.prompts import (
    SQL_REASONING_PROMPT,
)


class SQLReasoner:

    def __init__(self):

        self.llm = (
            LLMService()
        )

    def answer(
        self,
        question: str,
        rows,
    ):

        prompt = SQL_REASONING_PROMPT.format(
            question=question,
            rows=rows,
        )

        return self.llm.generate(
            prompt,
        )