from sqlalchemy.orm import Session
from app.search.service import (
    SearchService,
    )
from app.chat.prompt import (
    build_prompt,
)
from app.ai.gemini import (
    generate_response,
)
from app.chat.schemas import ChatResponse, CitationResponse, DebugResponse, RetrievedChunkResponse
from app.conversation.service import (
    ConversationService,
)

from app.query_rewrite.service import (
    QueryRewriteService,
)

class ChatService:

    def __init__(
        self,
        db: Session,
    ):

        self.search = SearchService(
            db,
        )

        self.conversation_service = (
            ConversationService(db)
        )

        self.query_rewriter = (
            QueryRewriteService()
        )


    def ask(
        self,
        organization_id: int,
        project_id: int,
        conversation_id: int | None,
        question: str,
        limit: int = 5,
        debug: bool = False,
    ):

        if conversation_id is None:

            conversation = (
                self.conversation_service.create_conversation(
                    organization_id,
                    project_id,
                    question,
                )
            )

        else:

            conversation = (
                self.conversation_service.get_conversation(
                    conversation_id,
                )
            )

        messages = (
            self.conversation_service.get_messages(
                conversation.id,
            )
        )

        history = []

        for message in messages:

            history.append(
                f"{message.role.value.title()}: {message.content}"
            )

        self.conversation_service.save_user_message(
            conversation.id,
            question,
        )

        rewritten_query = (
            self.query_rewriter.rewrite(
                history,
                question,
            )
        )

        chunks = self.search.search(
            organization_id,
            project_id,
            rewritten_query,
            limit,
        )

        context = [
            chunk.content
            for chunk, _, _ in chunks
        ]

        prompt = build_prompt(
            # question,
            rewritten_query,
            context,
            history,
        )

        citations = []

        for chunk, document, distance in chunks:

            citations.append(
                CitationResponse(
                    document_id=document.id,
                    document_name=document.original_filename,
                    chunk_index=chunk.chunk_index,
                    similarity_score=distance,
                )
            )


        retrieved_chunks = []

        for chunk, document, distance in chunks:

            retrieved_chunks.append(
                RetrievedChunkResponse(
                    document_name=document.original_filename,
                    chunk_index=chunk.chunk_index,
                    similarity_score=distance,
                    content=chunk.content,
                )
            )

        answer = generate_response(
            prompt,
        )

        debug_response = None

        if debug:

            debug_response = DebugResponse(
                prompt=prompt,
                retrieved_chunks=retrieved_chunks,
                rewritten_query=rewritten_query,
            )

        self.conversation_service.save_assistant_message(
            conversation.id,
            answer,
        )

        return ChatResponse(
            conversation_id=conversation.id,
            answer=answer,
            citations=citations,
            debug=debug_response,
        )