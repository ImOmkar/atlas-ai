
import json

from app.ai.gemini import (
    generate_execution_plan,
    generate_execution_response,
)

from app.agents.prompts import (
    EXECUTION_PLAN_PROMPT,
    EXECUTION_REASONING_PROMPT,
)

from app.agents.context import (
    ExecutionContext,
)

from app.tools.service import (
    ToolService,
)


class Executor:
    def __init__(self):

        self.tool_service = (
            ToolService()
        )

    def plan(
        self,
        question: str,
    ):

        prompt = EXECUTION_PLAN_PROMPT.format(
            question=question,
        )

        response = generate_execution_plan(
            prompt,
        )

        return json.loads(
            response,
        )

    def execute(
        self,
        plan: list,
    ):

        context = ExecutionContext()

        for step in plan:

            tool = step["tool"]

            arguments = step.get(
                "arguments",
                {},
            )

            resolved_arguments = {}

            for key, value in arguments.items():

                if isinstance(value, str):

                    for variable_name, variable_value in context.memory().items():

                        value = value.replace(
                            f"{{{{{variable_name}}}}}",
                            str(variable_value),
                        )

                resolved_arguments[key] = value

            result = self.tool_service.execute(
                tool,
                resolved_arguments,
            )

            output = step.get(
                "output",
            )

            if output:
                context.set(
                    output,
                    result,
                )

            context.add(
                tool,
                result,
            )

        return context

    def reason(
        self,
        question: str,
        context: ExecutionContext,
    ):
        history = json.dumps(
            context.all(),
            indent=2,
        )

        prompt = EXECUTION_REASONING_PROMPT.format(
            question=question,
            history=history,
        )

        return generate_execution_response(
            prompt,
        )

    def run(
        self,
        question: str,
    ):

        plan = self.plan(question)

        print("Execution Plan:", plan)

        context = self.execute(plan)

        answer = self.reason(
            question,
            context,
        )

        return answer




if __name__ == "__main__":

    # question = "Calculate GST on ₹25000 at 18%"

    # executor = Executor()

    # print(
    #     executor.run(question)
    # )


    plan = [
        {
            "tool": "calculator",
            "arguments": {
                "expression": "25000 * 18 / 100"
            },
            "output": "gst"
        },
        {
            "tool": "calculator",
            "arguments": {
                "expression": "{{gst}} + 1000"
            }
        }
    ]

    executor = Executor()

    context = executor.execute(plan)

    print(context.memory())
    print(context.all())
        