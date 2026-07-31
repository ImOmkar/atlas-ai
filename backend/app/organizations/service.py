from slugify import slugify

from app.organizations.models import Organization, OrganizationMember
from app.organizations.repository import OrganizationRepository
from app.organizations.exceptions import OrganizationMemberNotFoundError, OrganizationNotFoundError
from app.auth.user_repository import UserRepository
from app.auth.exceptions import UserNotFoundError
from app.auth.models import User
from app.organizations.enums import OrganizationRole

class OrganizationService:

    def __init__(
        self,
        db,
    ):
        self.organization_repository = OrganizationRepository(db)
        self.user_repository = UserRepository(db)

    def get_by_id(
        self,
        organization_id: int,
    ) -> Organization:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        return organization

    def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        return self.organization_repository.get_members(
            organization_id,
        )

    def add_member(
        self,
        organization_id: int,
        request,
    ) -> OrganizationMember:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        user = self.user_repository.get_user_by_id(
            request.user_id,
        )

        if user is None:
            raise UserNotFoundError()

        member = OrganizationMember(
            organization_id=organization_id,
            user_id=request.user_id,
            role=request.role,
        )

        return self.organization_repository.add_member(
            member,
        )


    def remove_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> None:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundError()

        member = self.organization_repository.get_member(
            organization_id,
            user_id,
        )

        if member is None:
            raise OrganizationMemberNotFoundError()

        self.organization_repository.delete_member(
            member,
        )


    def create(
        self,
        request,
        current_user: User,
    ) -> Organization:

        organization = Organization(
            name=request.name,
            slug=slugify(request.name),
        )

        organization = self.organization_repository.create(
            organization,
        )

        member = OrganizationMember(
            organization_id=organization.id,
            user_id=current_user.id,
            role=OrganizationRole.OWNER,
        )

        self.organization_repository.add_member(
            member,
        )

        return organization