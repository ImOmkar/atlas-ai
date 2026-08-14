from fastapi import APIRouter, Depends, Response, status
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

router = APIRouter(
    prefix="/organizations/{organization_id}/projects",
    tags=["Projects"],
)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_projects(
    organization_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.get_all(
        organization_id,
    )

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
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
    service = ProjectService(db)

    return service.get_by_id(
        organization_id,
        project_id,
    )

@router.post(
    "",
    response_model=ProjectResponse,
)
def create_project(
    organization_id: int,
    request: CreateProjectRequest,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        )
    ),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.create(
        organization_id,
        request,
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    organization_id: int,
    project_id: int,
    request: UpdateProjectRequest,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        )
    ),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.update(
        organization_id,
        project_id,
        request,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    organization_id: int,
    project_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        )
    ),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    service.delete(
        organization_id,
        project_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )