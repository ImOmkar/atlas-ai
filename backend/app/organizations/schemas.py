from pydantic import BaseModel, ConfigDict
from app.organizations.enums import OrganizationRole

class CreateOrganizationRequest(BaseModel):
    name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class AddOrganizationMemberRequest(BaseModel):
    user_id: int
    role: OrganizationRole = OrganizationRole.MEMBER


class OrganizationMemberResponse(BaseModel):
    id: int
    organization_id: int
    user_id: int
    role: OrganizationRole

    model_config = ConfigDict(
        from_attributes=True,
    )