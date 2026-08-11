

from app.proposals.models import ProposalRequirement


class ProposalRequirementRepository:

    def __init__(self, db):

        self.db = db

    def create(
        self,
        requirement: ProposalRequirement,
    ) -> ProposalRequirement:

        self.db.add(requirement)

        self.db.flush()

        self.db.refresh(requirement)

        return requirement

    def get_by_proposal_id(
        self,
        proposal_id: int,
    ) -> ProposalRequirement | None:

        return (
            self.db.query(
                ProposalRequirement
            )
            .filter(
                ProposalRequirement.proposal_id
                == proposal_id,
            )
            .first()
        )


    def update(
        self,
        requirement: ProposalRequirement,
    ) -> ProposalRequirement:

        self.db.flush()

        self.db.refresh(
            requirement,
        )

        return requirement