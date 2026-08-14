from datetime import datetime

from pydantic import BaseModel


class ConversationListResponse(BaseModel):

    id: int

    title: str

    created_at: datetime

    updated_at: datetime


class ConversationMessageResponse(BaseModel):

    role: str

    content: str

    created_at: datetime


class ConversationResponse(BaseModel):

    id: int

    title: str

    created_at: datetime

    updated_at: datetime

    messages: list[ConversationMessageResponse]


class RenameConversationRequest(BaseModel):

    title: str