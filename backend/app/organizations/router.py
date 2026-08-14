from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.auth.models import User
from app.db.dependencies import get_db

from app.organizations.schemas import (
    AddOrganizationMemberRequest,
    CreateOrganizationRequest,
    OrganizationMemberResponse,
    OrganizationResponse,
)

from app.organizations.service import OrganizationService
from app.organizations.models import OrganizationMember
from app.organizations.dependencies import require_organization_roles
from app.organizations.enums import OrganizationRole

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
)
def create_organization(
    request: CreateOrganizationRequest,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    return service.create(
        request,
        current_user,
    )

@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.MEMBER,
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    return service.get_by_id(
        organization_id,
    )

@router.get(
    "/{organization_id}/members",
    response_model=list[OrganizationMemberResponse],
)
def get_members(
    organization_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.MEMBER,
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    return service.get_members(
        organization_id,
    )

@router.post(
    "/{organization_id}/members",
    response_model=OrganizationMemberResponse,
)
def add_member(
    organization_id: int,
    request: AddOrganizationMemberRequest,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    return service.add_member(
        organization_id,
        request,
    )

@router.delete(
    "/{organization_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    organization_id: int,
    user_id: int,
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        )
    ),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    service.remove_member(
        organization_id,
        user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )






# testing purpose only

@router.get("/{organization_id}/me")
def my_membership(
    current_member: OrganizationMember = Depends(
        require_organization_roles(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
            OrganizationRole.MEMBER,
        )
    ),
):
    return current_member