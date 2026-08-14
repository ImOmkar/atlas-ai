

from app.db.session import SessionLocal

from app.rfp_requirements.repository import (
    RFPRequirementRepository,
)

from app.proposals.requirement_repository import (
    ProposalRequirementRepository,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        rfp_repository = (
            RFPRequirementRepository(db)
        )

        proposal_repository = (
            ProposalRequirementRepository(db)
        )

        # -------------------------
        # RFP REQUIREMENT
        # -------------------------

        rfp_requirement = (
            rfp_repository.get_by_rfp_id(
                5,
            )
        )

        print(
            "RFP Requirement:",
            rfp_requirement,
        )

        if rfp_requirement:

            print(
                "RFP ID:",
                rfp_requirement.rfp_id,
            )

            print(
                "Title:",
                rfp_requirement.title,
            )

            print(
                "Mandatory:",
                len(
                    rfp_requirement.mandatory_requirements
                ),
            )

        # -------------------------
        # PROPOSAL REQUIREMENT
        # -------------------------

        proposal_requirement = (
            proposal_repository.get_by_proposal_id(
                6,
            )
        )

        print(
            "\nProposal Requirement:",
            proposal_requirement,
        )

        if proposal_requirement:

            print(
                "Proposal ID:",
                proposal_requirement.proposal_id,
            )

            print(
                "Executive Summary:",
                proposal_requirement.executive_summary,
            )

            print(
                "Project Team:",
                proposal_requirement.project_team,
            )

    finally:

        db.close()