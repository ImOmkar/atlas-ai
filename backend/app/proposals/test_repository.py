
from app.db.session import SessionLocal

from app.proposals.enums import (
    ProposalStatus,
)

from app.proposals.models import (
    Proposal,
)

from app.proposals.repository import (
    ProposalRepository,
)

from app.documents.models import Document
from app.projects.models import Project
from app.rfps.models import RFP

if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            ProposalRepository(db)
        )

        proposal = Proposal(
            project_id=1,
            rfp_id=5,
            document_id=22,
        )

        repository.create(
            proposal,
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

        fetched = (
            repository.get_by_id(
                project_id=999,
                proposal_id=proposal.id,
            )
        )

        print(
            "\nFetched Proposal:"
        )

        print(
            "ID:",
            fetched.id,
        )

        print(
            "Status:",
            fetched.status,
        )

    finally:

        db.close()