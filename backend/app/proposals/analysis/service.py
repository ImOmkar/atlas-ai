
import json
from string import Template

from app.llm.service import LLMService

from app.rfp_requirements.repository import (
    RFPRequirementRepository,
)

from app.proposals.requirement_repository import (
    ProposalRequirementRepository,
)

from app.proposals.analysis.prompts import (
    ANALYSIS_PROMPT,
)
from app.utils.llm import parse_llm_json

from app.proposals.analysis.repository import (
    ProposalAnalysisRepository,
)

from app.proposals.analysis.compliance_repository import (
    ProposalComplianceItemRepository,
)
from app.proposals.analysis.models import ProposalAnalysis, ProposalComplianceItem

class ProposalAnalysisService:

    def __init__(self, db):

        self.llm = LLMService()

        self.rfp_requirement_repository = (
            RFPRequirementRepository(db)
        )

        self.proposal_requirement_repository = (
            ProposalRequirementRepository(db)
        )

        self.analysis_repository = (
            ProposalAnalysisRepository(db)
        )

        self.compliance_repository = (
            ProposalComplianceItemRepository(db)
        )


    def get_by_proposal_id(
        self,
        proposal_id: int,
    ):
        analyses = (
            self.analysis_repository
            .get_all(
                proposal_id,
            )
        )

        if not analyses:
            return None

        return analyses[0]

    def analyze(
        self,
        rfp_id: int,
        proposal_id: int,
    ) -> dict:

        rfp_requirement = (
            self.rfp_requirement_repository
            .get_by_rfp_id(
                rfp_id,
            )
        )

        if rfp_requirement is None:

            raise ValueError(
                "RFP requirements not found."
            )

        proposal_requirement = (
            self.proposal_requirement_repository
            .get_by_proposal_id(
                proposal_id,
            )
        )

        if proposal_requirement is None:

            raise ValueError(
                "Proposal requirements not found."
            )

        rfp_data = {
            "title": rfp_requirement.title,
            "client": rfp_requirement.client,
            "submission_deadline": (
                rfp_requirement.submission_deadline
            ),
            "project_overview": (
                rfp_requirement.project_overview
            ),
            "mandatory_requirements": (
                rfp_requirement.mandatory_requirements
            ),
            "technical_requirements": (
                rfp_requirement.technical_requirements
            ),
            "functional_requirements": (
                rfp_requirement.functional_requirements
            ),
            "deliverables": (
                rfp_requirement.deliverables
            ),
            "commercial_requirements": (
                rfp_requirement.commercial_requirements
            ),
            "eligibility_requirements": (
                rfp_requirement.eligibility_requirements
            ),
        }

        proposal_data = {
            "executive_summary": (
                proposal_requirement.executive_summary
            ),
            "company_profile": (
                proposal_requirement.company_profile
            ),
            "understanding_of_requirements": (
                proposal_requirement
                .understanding_of_requirements
            ),
            "proposed_solution": (
                proposal_requirement.proposed_solution
            ),
            "technical_approach": (
                proposal_requirement.technical_approach
            ),
            "implementation_approach": (
                proposal_requirement
                .implementation_approach
            ),
            "project_team": (
                proposal_requirement.project_team
            ),
            "relevant_experience": (
                proposal_requirement
                .relevant_experience
            ),
            "deliverables": (
                proposal_requirement.deliverables
            ),
            "support_model": (
                proposal_requirement.support_model
            ),
            "commercial_proposal": (
                proposal_requirement
                .commercial_proposal
            ),
            "assumptions": (
                proposal_requirement.assumptions
            ),
            "exceptions": (
                proposal_requirement.exceptions
            ),
            "client_references": (
                proposal_requirement
                .client_references
            ),
        }

        prompt = Template(
            ANALYSIS_PROMPT
        ).substitute(
            rfp_requirements=json.dumps(
                rfp_data,
                indent=2,
            ),
            proposal_requirements=json.dumps(
                proposal_data,
                indent=2,
            ),
        )

        response = self.llm.generate(
            prompt,
        )

        print(
            "\nRAW ANALYSIS RESPONSE:"
        )

        print(response)

        parsed_response = (
            parse_llm_json(response)
        )

        return parsed_response



    def analyze_and_save(
        self,
        rfp_id: int,
        proposal_id: int,
    ) -> ProposalAnalysis:

        existing_analysis = (
            self.analysis_repository
            .get_by_proposal_id(
                proposal_id,
            )
        )

        if existing_analysis is not None:
            return existing_analysis

        result = self.analyze(
            rfp_id=rfp_id,
            proposal_id=proposal_id,
        )

        analysis = ProposalAnalysis(
            proposal_id=proposal_id,
            overall_score=result.get(
                "overall_score",
            ),
            summary=result.get(
                "summary",
            ),
        )

        analysis = (
            self.analysis_repository.create(
                analysis,
            )
        )

        # raise ValueError(
        #     "TEST: intentional compliance persistence failure"
        # )

        for item in result.get(
            "items",
            [],
        ):

            compliance_item = ProposalComplianceItem(
                analysis_id=analysis.id,

                category=item.get(
                    "category",
                ),

                requirement=item.get(
                    "requirement",
                ),

                proposal_response=item.get(
                    "proposal_response",
                ),

                status=item.get(
                    "status",
                ),

                evidence=item.get(
                    "evidence",
                ),

                remarks=item.get(
                    "remarks",
                ),
            )

            self.compliance_repository.create(
                compliance_item,
            )

        # for index, item in enumerate(
        #     result.get(
        #         "items",
        #         [],
        #     )
        # ):
        #     compliance_item = ProposalComplianceItem(
        #         analysis_id=analysis.id,

        #         category=item.get(
        #             "category",
        #         ),

        #         requirement=item.get(
        #             "requirement",
        #         ),

        #         proposal_response=item.get(
        #             "proposal_response",
        #         ),

        #         status=item.get(
        #             "status",
        #         ),

        #         evidence=item.get(
        #             "evidence",
        #         ),

        #         remarks=item.get(
        #             "remarks",
        #         ),
        #     )

        #     self.compliance_repository.create(
        #         compliance_item,
        #     )

        #     if index == 0:
        #         raise ValueError(
        #             "TEST: intentional failure after first compliance item"
        #         )

        return analysis