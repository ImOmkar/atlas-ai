
from app.db.session import SessionLocal

from app.proposals.service import (
    ProposalService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        service = ProposalService(db)

        proposal = (
            service.get_by_id(
                project_id=1,
                proposal_id=7,
            )
        )

        print(
            "Before:",
            proposal.status,
        )

        proposal = service.process(
            proposal,
        )

        print(
            "After:",
            proposal.status,
        )

    finally:

        db.close()