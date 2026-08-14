
from app.proposals.models import (
    ProposalRequirement,
)

from app.proposals.generator import (
    ProposalGenerator,
)

from app.proposals.requirement_repository import (
    ProposalRequirementRepository,
)


class ProposalRequirementService:

    def __init__(self, db):

        self.db = db

        self.generator = (
            ProposalGenerator()
        )

        self.repository = (
            ProposalRequirementRepository(db)
        )

    def extract_and_save(
        self,
        proposal_id: int,
        document: str,
    ) -> ProposalRequirement:

        data = self.generator.generate(
            document,
        )

        existing = (
            self.repository.get_by_proposal_id(
                proposal_id,
            )
        )

        if existing:

            existing.executive_summary = (
                data.get("executive_summary")
            )

            existing.company_profile = (
                data.get("company_profile")
            )

            existing.understanding_of_requirements = (
                data.get(
                    "understanding_of_requirements"
                )
            )

            existing.proposed_solution = (
                data.get("proposed_solution")
            )

            existing.technical_approach = (
                data.get("technical_approach")
            )

            existing.implementation_approach = (
                data.get("implementation_approach")
            )

            existing.project_team = (
                data.get("project_team", [])
            )

            existing.relevant_experience = (
                data.get("relevant_experience", [])
            )

            existing.deliverables = (
                data.get("deliverables", [])
            )

            existing.support_model = (
                data.get("support_model")
            )

            existing.commercial_proposal = (
                data.get("commercial_proposal", [])
            )

            existing.assumptions = (
                data.get("assumptions", [])
            )

            existing.exceptions = (
                data.get("exceptions", [])
            )

            existing.client_references = (
                data.get("client_references", [])
            )

            return self.repository.update(
                existing,
            )

        requirement = ProposalRequirement(
            proposal_id=proposal_id,

            executive_summary=data.get(
                "executive_summary"
            ),

            company_profile=data.get(
                "company_profile"
            ),

            understanding_of_requirements=data.get(
                "understanding_of_requirements"
            ),

            proposed_solution=data.get(
                "proposed_solution"
            ),

            technical_approach=data.get(
                "technical_approach"
            ),

            implementation_approach=data.get(
                "implementation_approach"
            ),

            project_team=data.get(
                "project_team",
                [],
            ),

            relevant_experience=data.get(
                "relevant_experience",
                [],
            ),

            deliverables=data.get(
                "deliverables",
                [],
            ),

            support_model=data.get(
                "support_model"
            ),

            commercial_proposal=data.get(
                "commercial_proposal",
                [],
            ),

            assumptions=data.get(
                "assumptions",
                [],
            ),

            exceptions=data.get(
                "exceptions",
                [],
            ),

            client_references=data.get(
                "client_references",
                [],
            ),
        )

        return self.repository.create(
            requirement,
        )


    # def update(
    #     self,
    #     requirement: ProposalRequirement,
    # ) -> ProposalRequirement:

    #     self.db.commit()

    #     self.db.refresh(
    #         requirement,
    #     )

    #     return requirement