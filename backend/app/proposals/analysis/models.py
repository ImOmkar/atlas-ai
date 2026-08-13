
from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    Text,
    String,
    Enum
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.proposals.analysis.enums import ComplianceStatus


class ProposalAnalysis(
    TimestampMixin,
    Base,
):

    __tablename__ = "proposal_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
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

    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )



class ProposalComplianceItem(
    TimestampMixin,
    Base,
):

    __tablename__ = "proposal_compliance_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey(
            "proposal_analyses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    requirement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    proposal_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ComplianceStatus] = mapped_column(
        Enum(ComplianceStatus),
        nullable=False,
    )

    evidence: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )