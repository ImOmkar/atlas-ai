

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

router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
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

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Proposal processing failed.",
        )