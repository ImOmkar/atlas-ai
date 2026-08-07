from app.llm.service import (
    LLMService,
)

from app.sql.prompts import (
    SQL_GENERATION_PROMPT,
)


class SQLGenerator:

    def __init__(self):

        self.llm = (
            LLMService()
        )

    def generate(
        self,
        question: str,
    ):

        prompt = (
            SQL_GENERATION_PROMPT.format(
                question=question,
            )
        )

        query = self.llm.generate(
            prompt,
        )

        query = (
            query
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        return query



# if __name__ == "__main__":
    
#     sql_generator = SQLGenerator()

#     print(
#         sql_generator.generate(
#             "Count all documents."
#         )
#     )