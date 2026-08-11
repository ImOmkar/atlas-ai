
from app.rfps.repository import RFPRepository
from app.rfp_requirements.repository import (
    RFPRequirementRepository,
)


class RFPRequirementService:

    def __init__(self, db):

        self.rfp_repository = (
            RFPRepository(db)
        )

        self.requirement_repository = (
            RFPRequirementRepository(db)
        )

    def get_for_rfp(
        self,
        project_id: int,
        rfp_id: int,
    ):

        rfp = (
            self.rfp_repository.get_by_id(
                project_id=project_id,
                rfp_id=rfp_id,
            )
        )

        if rfp is None:

            raise ValueError(
                "RFP not found."
            )

        requirement = (
            self.requirement_repository
            .get_by_rfp_id(
                rfp.id,
            )
        )

        if requirement is None:

            raise ValueError(
                "RFP requirements not found."
            )

        return requirement