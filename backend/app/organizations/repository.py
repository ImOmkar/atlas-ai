from sqlalchemy.orm import Session

from app.organizations.models import Organization

from app.organizations.models import OrganizationMember

class OrganizationRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_user_membership(
        self,
        organization_id: int,
        user_id: int,
    ) -> OrganizationMember | None:
        return (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
            .first()
        )


    def get_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        return (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id,
            )
            .first()
        )

    def get_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> OrganizationMember | None:
        return (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
            .first()
        )

    def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        return (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
            )
            .all()
        )

    def add_member(
        self,
        member: OrganizationMember,
    ) -> OrganizationMember:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)

        return member

    def delete_member(
            self,
            member: OrganizationMember,
        ) -> None:
            self.db.delete(member)
            self.db.commit()

    def create(
        self,
        organization: Organization,
    ) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization