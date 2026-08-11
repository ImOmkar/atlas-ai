

from sqlalchemy.orm import Session

from app.proposals.analysis.models import (
    ProposalAnalysis,
)


class ProposalAnalysisRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db


    def get_by_proposal_id(
        self,
        proposal_id: int,
    ) -> ProposalAnalysis | None:

        return (
            self.db.query(
                ProposalAnalysis,
            )
            .filter(
                ProposalAnalysis.proposal_id
                == proposal_id,
            )
            .order_by(
                ProposalAnalysis.created_at.desc(),
            )
            .first()
        )
    
    def create(
        self,
        analysis: ProposalAnalysis,
    ) -> ProposalAnalysis:

        self.db.add(
            analysis,
        )

        self.db.flush()

        self.db.refresh(
            analysis,
        )

        return analysis

    def get_by_id(
        self,
        proposal_id: int,
        analysis_id: int,
    ) -> ProposalAnalysis | None:

        return (
            self.db.query(
                ProposalAnalysis,
            )
            .filter(
                ProposalAnalysis.id == analysis_id,
                ProposalAnalysis.proposal_id
                == proposal_id,
            )
            .first()
        )

    def get_all(
        self,
        proposal_id: int,
    ) -> list[ProposalAnalysis]:

        return (
            self.db.query(
                ProposalAnalysis,
            )
            .filter(
                ProposalAnalysis.proposal_id
                == proposal_id,
            )
            .order_by(
                ProposalAnalysis.created_at.desc(),
            )
            .all()
        )