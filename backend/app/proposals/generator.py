

import json
from string import Template

from app.llm.service import LLMService

from app.proposals.prompts import (
    PROPOSAL_EXTRACTION_PROMPT,
)
from app.utils.llm import parse_llm_json
from app.proposals.schemas import ProposalExtractionSchema


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

        parsed_response = parse_llm_json(response)

        # parsed_response = parse_llm_json(
        #     '{"unexpected_field": "test"}'
        # )

        # return parsed_response

        validated_response = (
            ProposalExtractionSchema.model_validate(
                parsed_response
            )
        )

        return validated_response.model_dump()