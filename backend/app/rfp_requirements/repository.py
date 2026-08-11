
from sqlalchemy.orm import Session

from app.rfps.models import (
    RFPRequirement,
)


class RFPRequirementRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        requirement: RFPRequirement,
    ) -> RFPRequirement:

        self.db.add(
            requirement
        )

        self.db.commit()

        self.db.refresh(
            requirement
        )

        return requirement

    def get_by_rfp_id(
        self,
        rfp_id: int,
    ) -> RFPRequirement | None:

        return (
            self.db.query(
                RFPRequirement
            )
            .filter(
                RFPRequirement.rfp_id == rfp_id
            )
            .first()
        )

    def update(
        self,
        requirement: RFPRequirement,
    ) -> RFPRequirement:

        self.db.commit()

        self.db.refresh(
            requirement
        )

        return requirement