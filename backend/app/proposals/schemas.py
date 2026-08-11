from datetime import datetime

from pydantic import BaseModel, Field

from app.proposals.enums import ProposalStatus
from app.proposals.analysis.enums import ComplianceStatus


class ProposalRequirementResponse(
    BaseModel
):

    model_config = {
        "from_attributes": True,
    }

    executive_summary: str | None = None
    company_profile: str | None = None
    understanding_of_requirements: str | None = None
    proposed_solution: str | None = None
    technical_approach: str | None = None
    implementation_approach: str | None = None

    project_team: list = Field(default_factory=list)
    relevant_experience: list = Field(default_factory=list)
    deliverables: list = Field(default_factory=list)

    support_model: str | None = None

    commercial_proposal: list = Field(default_factory=list)
    assumptions: list = Field(default_factory=list)
    exceptions: list = Field(default_factory=list)
    client_references: list = Field(default_factory=list)


class ProposalAnalysisResponse(
    BaseModel
):

    model_config = {
        "from_attributes": True,
    }


    id: int
    overall_score: float | None = None
    summary: str | None = None


class ProposalComplianceItemResponse(
    BaseModel
):

    model_config = {
        "from_attributes": True,
    }


    id: int
    category: str
    requirement: str
    proposal_response: str | None = None
    status: ComplianceStatus
    evidence: str | None = None
    remarks: str | None = None


class ProposalDetailsResponse(
    BaseModel
):

    model_config = {
        "from_attributes": True,
    }

    
    id: int
    project_id: int
    rfp_id: int
    document_id: int
    status: ProposalStatus

    requirements: (
        ProposalRequirementResponse | None
    ) = None

    analysis: (
        ProposalAnalysisResponse | None
    ) = None

    compliance_items: list[
        ProposalComplianceItemResponse
    ] = Field(default_factory=list)



class ProposalAnalysisDetailsResponse(BaseModel):

    model_config = {
        "from_attributes": True,
    }

    id: int
    proposal_id: int
    overall_score: float | None = None
    summary: str | None = None

    compliance_items: list[
        ProposalComplianceItemResponse
    ] = Field(default_factory=list)


class ProposalAnalysisSummaryResponse(
    BaseModel
):

    proposal_id: int
    analysis_id: int

    overall_score: float | None = None

    total_requirements: int
    compliant: int
    partially_compliant: int
    non_compliant: int
    not_addressed: int

    compliance_percentage: float

    summary: str | None = None



class ProposalComplianceItemPageResponse(
    BaseModel
):

    items: list[
        ProposalComplianceItemResponse
    ]

    total: int
    page: int
    page_size: int
    total_pages: int