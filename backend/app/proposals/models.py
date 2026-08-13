
from sqlalchemy import (
    JSON,
    Enum,
    ForeignKey,
    Text,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base
from app.db.mixins import TimestampMixin

from app.proposals.enums import (
    ProposalStatus,
)


class Proposal(
    TimestampMixin,
    Base,
):

    __tablename__ = "proposals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    rfp_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rfps.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status: Mapped[ProposalStatus] = mapped_column(
        Enum(ProposalStatus),
        nullable=False,
        default=ProposalStatus.PENDING,
    )




class ProposalRequirement(
    TimestampMixin,
    Base,
):

    __tablename__ = "proposal_requirements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    proposal_id: Mapped[int] = mapped_column(
        ForeignKey(
            "proposals.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    executive_summary: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    company_profile: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    understanding_of_requirements: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    proposed_solution: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    technical_approach: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    implementation_approach: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    project_team: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    relevant_experience: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    deliverables: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    support_model: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    commercial_proposal: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    assumptions: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    exceptions: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    client_references: Mapped[
        list
    ] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )