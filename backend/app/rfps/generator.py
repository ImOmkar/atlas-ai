import json
from string import Template

from app.llm.service import LLMService
from app.rfps.prompts import (
    RFP_EXTRACTION_PROMPT,
)


class RFPGenerator:

    def __init__(self):

        self.llm = (
            LLMService()
        )

    def generate(
        self,
        document: str,
    ) -> dict:

        # prompt = RFP_EXTRACTION_PROMPT.format(
        #     document=document,
        # )

        prompt = Template(RFP_EXTRACTION_PROMPT).substitute(
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