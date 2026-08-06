
from app.ai.gemini import (
    plan_task,
)

from app.agents.prompts import (
    PLANNER_PROMPT,
)
from app.agents.enums import AgentTask

class Planner:

    def plan(
        self,
        user_input: str,
    ):

        prompt = PLANNER_PROMPT.format(
            user_input=user_input,
        )

        task = plan_task(
            prompt,
        )

        return AgentTask(
            task.lower(),
        )





# if __name__ == "__main__":

#     planner = Planner()

#     test = planner.plan(
#         "Summarize this document"
#     )

#     print(test)