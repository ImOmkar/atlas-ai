

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.proposals.service import (
    ProposalService,
)

from app.proposals.schemas import (
    ProposalDetailsResponse,
)

from app.proposals.analysis.enums import (
    ComplianceStatus,
)

from app.proposals.schemas import (
    ProposalAnalysisResponse,
    ProposalComplianceItemResponse,
    ProposalDetailsResponse,
    ProposalRequirementResponse,
    ProposalAnalysisSummaryResponse,
    ProposalComplianceItemPageResponse
)
from app.proposals.exceptions import ProposalProcessingError

router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
)


@router.post(
    "/",
)
def create_proposal(
    project_id: int,
    rfp_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):

    service = ProposalService(db)

    try:

        proposal = (
            service.create_from_document(
                project_id=project_id,
                rfp_id=rfp_id,
                document_id=document_id,
            )
        )

        db.commit()

        return {
            "id": proposal.id,
            "project_id": proposal.project_id,
            "rfp_id": proposal.rfp_id,
            "document_id": proposal.document_id,
            "status": proposal.status.value,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/{proposal_id}/process",
)
def process_proposal(
    proposal_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = ProposalService(db)

    proposal = service.get_by_id(
        project_id=project_id,
        proposal_id=proposal_id,
    )

    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail="Proposal not found.",
        )

    try:

        proposal = service.process(
            proposal,
        )

        return {
            "id": proposal.id,
            "project_id": proposal.project_id,
            "rfp_id": proposal.rfp_id,
            "document_id": proposal.document_id,
            "status": proposal.status.value,
        }

    except ProposalProcessingError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Proposal processing failed.",
        )

@router.get(
    "/{proposal_id}/analysis/summary",
    response_model=ProposalAnalysisSummaryResponse,
)
def get_proposal_analysis_summary(
    proposal_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = ProposalService(db)

    try:

        return service.get_analysis_summary(
            project_id=project_id,
            proposal_id=proposal_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/{proposal_id}/analysis",
    response_model=ProposalAnalysisResponse,
)
def get_proposal_analysis(
    proposal_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = ProposalService(db)

    try:

        analysis = service.get_analysis(
            project_id=project_id,
            proposal_id=proposal_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return analysis



@router.get(
    "/{proposal_id}/analysis/compliance",
    response_model=ProposalComplianceItemPageResponse,
)
def get_proposal_compliance(
    proposal_id: int,
    project_id: int,
    page: int = 1,
    page_size: int = 20,
    status: ComplianceStatus | None = None,
    db: Session = Depends(get_db),
):

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than or equal to 1.",
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=400,
            detail="page_size must be between 1 and 100.",
        )

    service = ProposalService(db)

    try:

        return service.get_compliance_items_paginated(
            project_id=project_id,
            proposal_id=proposal_id,
            page=page,
            page_size=page_size,
            status=status,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/{proposal_id}",
    response_model=ProposalDetailsResponse,
)
def get_proposal(
    proposal_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = ProposalService(db)

    try:

        return service.get_details(
            project_id=project_id,
            proposal_id=proposal_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )