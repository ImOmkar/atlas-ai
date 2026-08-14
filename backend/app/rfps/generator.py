import json
from string import Template

from app.llm.service import LLMService
from app.rfps.prompts import (
    RFP_EXTRACTION_PROMPT,
)
from app.utils.llm import parse_llm_json


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

        parsed_response = parse_llm_json(response)

        return parsed_response