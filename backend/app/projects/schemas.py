from pydantic import BaseModel, ConfigDict


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    slug: str
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateProjectRequest(BaseModel):
    name: str | None = None
    description: str | None = None