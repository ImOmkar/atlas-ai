

import json
from string import Template

from app.llm.service import LLMService

from app.proposals.prompts import (
    PROPOSAL_EXTRACTION_PROMPT,
)


class ProposalGenerator:

    def __init__(self):

        self.llm = LLMService()

    def generate(
        self,
        document: str,
    ) -> dict:

        prompt = Template(
            PROPOSAL_EXTRACTION_PROMPT
        ).substitute(
            document=document,
        )

        response = self.llm.generate(
            prompt,
        )

        print(
            "\nRAW LLM RESPONSE:"
        )

        print(
            response
        )

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(
            response
        )