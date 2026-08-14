from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.rfps.service import RFPService
from app.rfps.schemas import (
    RFPResponse,
    RFPRequirementResponse,
)

from app.rfps.analysis import (
    RFPAnalysisService,
)

from app.rfps.schemas import (
    RFPAnalysisResponse,
)

router = APIRouter(
    prefix="/rfps",
    tags=["RFP"],
)

@router.get(
    "/{rfp_id}",
    response_model=RFPResponse,
)
def get_rfp(
    rfp_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = RFPService(db)

    try:

        rfp, requirement = (
            service.get(
                project_id=project_id,
                rfp_id=rfp_id,
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    requirement_response = None

    if requirement:

        requirement_response = (
            RFPRequirementResponse(
                title=requirement.title,
                client=requirement.client,
                submission_deadline=(
                    requirement.submission_deadline
                ),
                project_overview=(
                    requirement.project_overview
                ),
                mandatory_requirements=(
                    requirement.mandatory_requirements
                ),
                technical_requirements=(
                    requirement.technical_requirements
                ),
                functional_requirements=(
                    requirement.functional_requirements
                ),
                deliverables=(
                    requirement.deliverables
                ),
                evaluation_criteria=(
                    requirement.evaluation_criteria
                ),
                commercial_requirements=(
                    requirement.commercial_requirements
                ),
                eligibility_requirements=(
                    requirement.eligibility_requirements
                ),
            )
        )

    return RFPResponse(
        id=rfp.id,
        project_id=rfp.project_id,
        document_id=rfp.document_id,
        status=rfp.status.value,
        created_at=rfp.created_at,
        updated_at=rfp.updated_at,
        requirements=requirement_response,
    )


@router.get(
    "/{rfp_id}/analysis",
    response_model=RFPAnalysisResponse,
)
def get_rfp_analysis(
    rfp_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = RFPAnalysisService(db)

    try:

        return service.analyze(
            project_id=project_id,
            rfp_id=rfp_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    

@router.post(
    "/",
)
def create_rfp(
    project_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):

    service = RFPService(db)

    try:

        rfp = service.create_from_document(
            project_id=project_id,
            document_id=document_id,
        )

        return {
            "id": rfp.id,
            "project_id": rfp.project_id,
            "document_id": rfp.document_id,
            "status": rfp.status,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )