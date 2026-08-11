

from app.proposals.models import Proposal


class ProposalRepository:

    def __init__(self, db):

        self.db = db

    def create(
        self,
        proposal: Proposal,
    ) -> Proposal:

        self.db.add(proposal)

        self.db.flush()

        self.db.refresh(proposal)

        return proposal

    def get_by_id(
        self,
        project_id: int,
        proposal_id: int,
    ) -> Proposal | None:

        return (
            self.db.query(Proposal)
            .filter(
                Proposal.id == proposal_id,
                Proposal.project_id == project_id,
            )
            .first()
        )

    def update(
        self,
        proposal: Proposal,
    ) -> Proposal:

        self.db.flush()

        self.db.refresh(
            proposal,
        )

        return proposal