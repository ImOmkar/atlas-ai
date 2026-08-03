from sqlalchemy.orm import Session

from app.conversation.enums import (
    MessageRole,
)

from app.conversation.models import (
    Conversation,
    ConversationMessage,
)

from app.conversation.repository import (
    ConversationRepository,
)


class ConversationService:

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            ConversationRepository(db)
        )


    def create_conversation(
        self,
        organization_id: int,
        project_id: int,
        title: str,
    ) -> Conversation:

        conversation = Conversation(
            organization_id=organization_id,
            project_id=project_id,
            title=title,
        )

        return self.repository.create_conversation(
            conversation,
        )


    def save_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> ConversationMessage:

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
        )

        return self.repository.create_message(
            message,
        )


    def save_assistant_message(
        self,
        conversation_id: int,
        content: str,
    ) -> ConversationMessage:

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=content,
        )

        return self.repository.create_message(
            message,
        )


    def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        return self.repository.get_conversation_by_id(
            conversation_id,
        )


    def get_messages(
        self,
        conversation_id: int,
    ) -> list[ConversationMessage]:

        return self.repository.get_messages(
            conversation_id,
        )


    def list_project_conversations(
        self,
        organization_id: int,
        project_id: int,
    ) -> list[Conversation]:

        return (
            self.repository.list_project_conversations(
                organization_id,
                project_id,
            )
        )


    def rename_conversation(
        self,
        conversation_id: int,
        title: str,
    ) -> Conversation:

        conversation = (
            self.repository.get_conversation_by_id(
                conversation_id,
            )
        )

        conversation.title = title

        return self.repository.update_conversation(
            conversation,
        )



    def delete_conversation(
        self,
        conversation_id: int,
    ) -> None:

        conversation = (
            self.repository.get_conversation_by_id(
                conversation_id,
            )
        )

        self.repository.delete_conversation(
            conversation,
        )