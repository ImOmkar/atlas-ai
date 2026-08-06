from sqlalchemy.orm import Session

from app.agents.planner import (
    Planner,
    AgentTask,
)

from app.chat.service import (
    ChatService,
)
from app.summarization.service import SummarizationService
from app.extraction.service import ExtractionService
from app.agents.tool_selector import (
    ToolSelector,
)

from app.tools.service import (
    ToolService,
)
from app.agents.enums import ToolDecision
from app.agents.prompts import TOOL_RESPONSE_PROMPT
from app.ai.gemini import generate_tool_response

from app.agents.tool_argument_generator import (
    ToolArgumentGenerator,
)

from app.agents.executor import (
    Executor,
)

class AgentService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.planner = (
            Planner()
        )

        self.chat_service = (
            ChatService(
                db,
            )
        )

        self.tool_selector = (
            ToolSelector()
        )

        self.tool_service = (
            ToolService()
        )

        self.argument_generator = (
            ToolArgumentGenerator()
        )

        self.executor = (
            Executor()
        )

    def run(
        self,
        organization_id: int,
        project_id: int,
        conversation_id: int | None,
        document_id: int | None,
        question: str,
        extraction_schema: dict | None = None,
        limit: int = 5,
        debug: bool = False,
    ):

        task = self.planner.plan(
            question,
        )

        if task == AgentTask.CHAT:

            tool = self.tool_selector.choose(
                question,
            )

            print(tool)

            if tool == ToolDecision.NONE:

                return self.chat_service.ask(
                    organization_id,
                    project_id,
                    conversation_id,
                    question,
                    limit,
                    debug,
                )

            # if tool == ToolDecision.CALCULATOR:

            #     arguments = (
            #         self.argument_generator.generate(
            #             "calculator",
            #             question,
            #         )
            #     )

            #     result = self.tool_service.execute(
            #         "calculator",
            #         arguments,
            #     )

            #     print(result)

            #     prompt = TOOL_RESPONSE_PROMPT.format(
            #             question=question,
            #             tool="calculator",
            #             result=result,
            #         )

            #     answer = generate_tool_response(
            #             prompt,
            #         )

            #     return {
            #             "answer": answer,
            #         }

            if tool == ToolDecision.CALCULATOR:

                answer = self.executor.run(
                    question,
                )

                return {
                    "answer": answer,
                }

                                    
        if task == AgentTask.SUMMARIZE:

            summary_service = (
                SummarizationService(
                    self.db,
                )
            )

            return summary_service.summarize(
                document_id,
            )

        if task == AgentTask.EXTRACT:

            extraction_service = (
                ExtractionService(
                    self.db,
                )
            )

            return extraction_service.extract(
                document_id,
                extraction_schema,
            )


        if task == AgentTask.COMPARE:

            return {
                "task": "compare",
                "message": "Not implemented yet."
            }


        raise ValueError(
            "Unknown task."
        )