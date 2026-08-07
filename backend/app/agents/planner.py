
from app.agents.prompts import (
    PLANNER_PROMPT,
)
from app.agents.enums import AgentTask
from app.llm.service import LLMService

class Planner:

    def __init__(self):

        self.llm = (
            LLMService()
        )

    def plan(
        self,
        user_input: str,
    ):

        prompt = PLANNER_PROMPT.format(
            user_input=user_input,
        )

        task = self.llm.generate(
            prompt,
        ).strip()

        return AgentTask(
            task.lower(),
        )





# if __name__ == "__main__":

#     planner = Planner()

#     test = planner.plan(
#         "How many casual leaves?"
#     )

#     print(test)