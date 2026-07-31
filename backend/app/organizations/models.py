
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Enum
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.db.mixins import TimestampMixin

from app.organizations.enums import OrganizationRole

class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )


class OrganizationMember(TimestampMixin, Base):
    __tablename__ = "organization_members"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole),
        nullable=False,
        default=OrganizationRole.MEMBER,
    )