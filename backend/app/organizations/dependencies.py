from fastapi import Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.db.dependencies import get_db

from app.organizations.enums import OrganizationRole
from app.organizations.models import OrganizationMember
from app.organizations.repository import OrganizationRepository
from app.organizations.exceptions import OrganizationMemberNotFoundError
from app.auth.exceptions import PermissionDeniedError


def require_organization_roles(
    *roles: OrganizationRole,
):
    def dependency(
        organization_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> OrganizationMember:

        repository = OrganizationRepository(db)

        member = repository.get_user_membership(
            organization_id,
            current_user.id,
        )

        if member is None:
            raise OrganizationMemberNotFoundError()

        if member.role not in roles:
            raise PermissionDeniedError()

        return member

    return dependency