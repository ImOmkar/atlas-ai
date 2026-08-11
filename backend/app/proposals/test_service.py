

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
            "Proposal ID:",
            proposal.id,
        )

        print(
            "Project ID:",
            proposal.project_id,
        )

        print(
            "RFP ID:",
            proposal.rfp_id,
        )

        print(
            "Document ID:",
            proposal.document_id,
        )

        print(
            "Status:",
            proposal.status,
        )

    finally:

        db.close()