from sqlalchemy.orm import Session

from app.conversation.models import (
    Conversation,
    ConversationMessage,
)

from sqlalchemy.orm import selectinload

class ConversationRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create_conversation(
        self,
        conversation: Conversation,
    ) -> Conversation:

        self.db.add(conversation)

        self.db.commit()

        self.db.refresh(conversation)

        return conversation

    def get_conversation_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        return (
            self.db.query(
                Conversation,
            )
            .options(
                selectinload(
                    Conversation.messages,
                )
            )
            .filter(
                Conversation.id == conversation_id,
            )
            .first()
        )

    def get_messages(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:

        return (
            self.db.query(
                ConversationMessage,
            )
            .filter(
                ConversationMessage.conversation_id == conversation_id,
            )
            .order_by(
                ConversationMessage.id.asc(),
            )
            .all()
        )

    def create_message(
        self,
        message: ConversationMessage,
    ) -> ConversationMessage:

        self.db.add(message)

        self.db.commit()

        self.db.refresh(message)

        return message

    def list_project_conversations(
        self,
        organization_id: int,
        project_id: int,
    ) -> list[Conversation]:

        return (
            self.db.query(
                Conversation,
            )
            .filter(
                Conversation.organization_id == organization_id,
                Conversation.project_id == project_id,
            )
            .order_by(
                Conversation.updated_at.desc(),
            )
            .all()
        )



    def update_conversation(
        self,
        conversation: Conversation,
    ) -> Conversation:

        self.db.commit()

        self.db.refresh(
            conversation,
        )

        return conversation


    def delete_conversation(
        self,
        conversation: Conversation,
    ) -> None:

        self.db.delete(
            conversation,
        )

        self.db.commit()