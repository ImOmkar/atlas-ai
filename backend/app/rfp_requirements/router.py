
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.rfp_requirements.service import (
    RFPRequirementService,
)


router = APIRouter(
    prefix="/rfps",
    tags=["RFP Requirements"],
)


@router.get(
    "/{rfp_id}/requirements",
)
def get_rfp_requirements(
    rfp_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = RFPRequirementService(db)

    try:

        requirement = (
            service.get_for_rfp(
                project_id=project_id,
                rfp_id=rfp_id,
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return {
        "rfp_id": rfp_id,
        "title": requirement.title,
        "client": requirement.client,
        "submission_deadline": (
            requirement.submission_deadline
        ),
        "project_overview": (
            requirement.project_overview
        ),
        "mandatory_requirements": (
            requirement.mandatory_requirements
        ),
        "technical_requirements": (
            requirement.technical_requirements
        ),
        "functional_requirements": (
            requirement.functional_requirements
        ),
        "deliverables": (
            requirement.deliverables
        ),
        "evaluation_criteria": (
            requirement.evaluation_criteria
        ),
        "commercial_requirements": (
            requirement.commercial_requirements
        ),
        "eligibility_requirements": (
            requirement.eligibility_requirements
        ),
    }