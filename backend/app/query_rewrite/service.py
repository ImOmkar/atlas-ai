\
from app.llm.service import LLMService


class QueryRewriteService:
    def __init__(
        self,
    ):
        self.llm = (
            LLMService()
        )

    def rewrite(
        self,
        history: list[str],
        question: str,
    ) -> str:


        conversation = "\n".join(
            history,
        )


        prompt = f"""
            You are a query rewriting assistant.

            Your job is ONLY to rewrite the user's latest question into a standalone question by using the previous conversation.

            Rules:
            - Preserve the exact meaning of the user's latest question.
            - Resolve pronouns and vague references using the conversation.
            - Do NOT generalize the question.
            - Do NOT answer the question.
            - Do NOT add extra information.
            - Return only the rewritten standalone question.

            Conversation:
            {conversation}

            Latest Question:
            {question}
        """

        return self.llm.generate(
            prompt,
        )
