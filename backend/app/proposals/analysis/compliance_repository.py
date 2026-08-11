
from sqlalchemy.orm import Session

from app.proposals.analysis.models import (
    ProposalComplianceItem,
)
from app.proposals.analysis.enums import ComplianceStatus


class ProposalComplianceItemRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def get_by_analysis_id_and_status(
        self,
        analysis_id: int,
        status: ComplianceStatus,
    ) -> list[ProposalComplianceItem]:

        return (
            self.db.query(
                ProposalComplianceItem,
            )
            .filter(
                ProposalComplianceItem.analysis_id
                == analysis_id,
                ProposalComplianceItem.status
                == status,
            )
            .order_by(
                ProposalComplianceItem.id,
            )
            .all()
        )

    def get_by_analysis_id_paginated(
        self,
        analysis_id: int,
        page: int,
        page_size: int,
        status: ComplianceStatus | None = None,
    ):
        query = (
            self.db.query(
                ProposalComplianceItem,
            )
            .filter(
                ProposalComplianceItem.analysis_id
                == analysis_id,
            )
        )

        if status is not None:

            query = query.filter(
                ProposalComplianceItem.status
                == status,
            )

        total = query.count()

        items = (
            query
            .order_by(
                ProposalComplianceItem.id,
            )
            .offset(
                (page - 1) * page_size,
            )
            .limit(page_size)
            .all()
        )

        return items, total

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