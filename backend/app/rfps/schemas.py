
from datetime import datetime

from pydantic import BaseModel, Field




class RFPRequirementResponse(
    BaseModel,
):

    title: str | None = None

    client: str | None = None

    submission_deadline: str | None = None

    project_overview: str | None = None

    mandatory_requirements: list = Field(
        default_factory=list,
    )

    technical_requirements: list = Field(
        default_factory=list,
    )

    functional_requirements: list = Field(
        default_factory=list,
    )

    deliverables: list = Field(
        default_factory=list,
    )

    evaluation_criteria: list = Field(
        default_factory=list,
    )

    commercial_requirements: list = Field(
        default_factory=list,
    )

    eligibility_requirements: list = Field(
        default_factory=list,
    )


class RFPResponse(
    BaseModel,
):

    id: int

    project_id: int

    document_id: int

    status: str

    created_at: datetime

    updated_at: datetime

    requirements: (
        RFPRequirementResponse
        | None
    ) = None



class EvaluationCriterion(
    BaseModel,
):

    criterion: str

    weightage: str


class RFPAnalysisSummary(
    BaseModel,
):

    mandatory_requirements_count: int

    technical_requirements_count: int

    functional_requirements_count: int

    deliverables_count: int

    evaluation_criteria_count: int

    commercial_requirements_count: int

    eligibility_requirements_count: int


class RFPAnalysisResponse(
    BaseModel,
):

    rfp_id: int

    title: str | None

    client: str | None

    submission_deadline: str | None

    summary: RFPAnalysisSummary

    evaluation_criteria: list[
        EvaluationCriterion
    ]