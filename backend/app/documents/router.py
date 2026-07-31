from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.organizations.dependencies import require_organization_roles
from app.organizations.enums import OrganizationRole
from app.organizations.models import OrganizationMember

from app.projects.schemas import (
    CreateProjectRequest,
    ProjectResponse,
    UpdateProjectRequest,
)

from app.projects.service import ProjectService
from app.documents.schemas import DocumentResponse
from app.documents.service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post(
    "",
    response_model=DocumentResponse,
)
def upload_document(
    organization_id: int,
    project_id: int,
    file: UploadFile = File(...),
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    return service.upload(
        organization_id,
        project_id,
        file,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(
    organization_id: int,
    project_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    return service.get_all(
        organization_id,
        project_id,
    )



@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    organization_id: int,
    project_id: int,
    document_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    return service.get_by_id(
        organization_id,
        project_id,
        document_id,
    )



@router.get(
    "/{document_id}/download",
)
def download_document(
    organization_id: int,
    project_id: int,
    document_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    document = service.download(
        organization_id,
        project_id,
        document_id,
    )

    return FileResponse(
        path=document.storage_path,
        filename=document.original_filename,
        media_type=document.content_type,
    )



@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    organization_id: int,
    project_id: int,
    document_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        )
    ),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)

    service.delete(
        organization_id,
        project_id,
        document_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )