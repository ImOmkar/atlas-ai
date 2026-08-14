

from app.db.session import SessionLocal

from app.proposals.models import (
    ProposalRequirement,
)

from app.proposals.requirement_repository import (
    ProposalRequirementRepository,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            ProposalRequirementRepository(db)
        )

        requirement = ProposalRequirement(
            proposal_id=1,

            executive_summary=(
                "Test executive summary."
            ),

            company_profile=(
                "Test company profile."
            ),

            understanding_of_requirements=(
                "Test understanding."
            ),

            proposed_solution=(
                "Test proposed solution."
            ),

            technical_approach=(
                "Test technical approach."
            ),

            implementation_approach=(
                "Test implementation approach."
            ),

            project_team=[
                "Project Manager",
                "Backend Developer",
            ],

            relevant_experience=[
                "Enterprise document management",
                "AI platform implementation",
            ],

            deliverables=[
                "Web application",
                "Technical documentation",
            ],

            support_model=(
                "12 months production support."
            ),

            commercial_proposal=[
                "Implementation cost",
                "Annual maintenance cost",
            ],

            assumptions=[
                "Client will provide required infrastructure."
            ],

            exceptions=[
                "Custom integrations are excluded."
            ],

            client_references=[
                "Client A",
                "Client B",
            ],
        )

        repository.create(
            requirement,
        )

        print(
            "Requirement ID:",
            requirement.id,
        )

        print(
            "Proposal ID:",
            requirement.proposal_id,
        )

        fetched = (
            repository.get_by_proposal_id(
                proposal_id=1,
            )
        )

        print(
            "\nFetched Requirement:"
        )

        print(
            "ID:",
            fetched.id,
        )

        print(
            "Proposal ID:",
            fetched.proposal_id,
        )

        print(
            "Executive Summary:",
            fetched.executive_summary,
        )

        print(
            "Project Team:",
            fetched.project_team,
        )

    finally:

        db.close()