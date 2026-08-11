
from sqlalchemy.orm import Session

from app.proposals.analysis.models import (
    ProposalComplianceItem,
)


class ProposalComplianceItemRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def create(
        self,
        item: ProposalComplianceItem,
    ) -> ProposalComplianceItem:

        self.db.add(
            item,
        )

        self.db.flush()

        self.db.refresh(
            item,
        )

        return item

    def get_by_analysis_id(
        self,
        analysis_id: int,
    ) -> list[ProposalComplianceItem]:

        return (
            self.db.query(
                ProposalComplianceItem,
            )
            .filter(
                ProposalComplianceItem.analysis_id
                == analysis_id,
            )
            .order_by(
                ProposalComplianceItem.id,
            )
            .all()
        )

    def get_by_id(
        self,
        analysis_id: int,
        item_id: int,
    ) -> ProposalComplianceItem | None:

        return (
            self.db.query(
                ProposalComplianceItem,
            )
            .filter(
                ProposalComplianceItem.id == item_id,
                ProposalComplianceItem.analysis_id
                == analysis_id,
            )
            .first()
        )