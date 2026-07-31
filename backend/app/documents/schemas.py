from pydantic import BaseModel, ConfigDict

from app.documents.enums import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    status: DocumentStatus

    model_config = ConfigDict(
        from_attributes=True,
    )