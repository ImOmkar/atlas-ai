
from sqlalchemy import (
    JSON,
    DateTime,
    String,
    Enum,
    ForeignKey,
    Integer,
    Text,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.documents.models import Document
from app.projects.models import Project
from app.rfps.enums import RFPStatus


class RFP(
    TimestampMixin,
    Base,
):

    __tablename__ = "rfps"

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

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status: Mapped[RFPStatus] = mapped_column(
        Enum(RFPStatus),
        nullable=False,
        default=RFPStatus.PROCESSING,
    )



class RFPRequirement(TimestampMixin, Base):

    __tablename__ = "rfp_requirements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    rfp_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rfps.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    title: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    client: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    submission_deadline: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    project_overview: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    mandatory_requirements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    technical_requirements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    functional_requirements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    deliverables: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    evaluation_criteria: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    commercial_requirements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    eligibility_requirements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )