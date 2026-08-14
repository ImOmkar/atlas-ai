from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.db.dependencies import get_db

from app.conversation.service import (
    ConversationService,
)

from app.conversation.schemas import (
    ConversationListResponse,
    ConversationResponse,
    RenameConversationRequest,
)


router = APIRouter(
    prefix="/organizations/{organization_id}/projects/{project_id}/conversations",
    tags=["Conversations"],
)



@router.get(
    "",
    response_model=list[ConversationListResponse],
)
def list_conversations(
    organization_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):

    service = ConversationService(
        db,
    )

    return service.list_project_conversations(
        organization_id,
        project_id,
    )



@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    organization_id: int,
    project_id: int,
    conversation_id: int,
    db: Session = Depends(get_db),
):

    service = ConversationService(
        db,
    )

    return service.get_conversation(
        conversation_id,
    )



@router.patch(
    "/{conversation_id}",
    response_model=ConversationListResponse,
)
def rename_conversation(
    organization_id: int,
    project_id: int,
    conversation_id: int,
    request: RenameConversationRequest,
    db: Session = Depends(get_db),
):

    service = ConversationService(
        db,
    )

    return service.rename_conversation(
        conversation_id,
        request.title,
    )



@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    organization_id: int,
    project_id: int,
    conversation_id: int,
    db: Session = Depends(get_db),
):

    service = ConversationService(
        db,
    )

    service.delete_conversation(
        conversation_id,
    )