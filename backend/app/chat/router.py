from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.chat.schemas import (
    ChatRequest,
)

from app.chat.service import (
    ChatService,
)

from app.agents.service import (
    AgentService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    service = AgentService(db)

    return service.run(
        request.organization_id,
        request.project_id,
        request.conversation_id,
        request.document_id,
        request.question,
        request.extraction_schema,
        request.limit,
        request.debug,
    )