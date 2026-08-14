
from app.db.session import SessionLocal

from app.proposals.service import (
    ProposalService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        service = ProposalService(db)

        proposal = service.create_from_document(
            project_id=1,
            rfp_id=5,
            document_id=23,
        )

        print(
            "Created Proposal:",
            proposal.id,
        )

        proposal = service.process(
            proposal,
        )

        print(
            "\nPROCESSING COMPLETE"
        )

        print(
            "Proposal ID:",
            proposal.id,
        )

        print(
            "Status:",
            proposal.status,
        )

    finally:

        db.close()