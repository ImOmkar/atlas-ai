from pydantic import BaseModel

class ChatRequest(BaseModel):

    organization_id: int

    project_id: int

    conversation_id: int | None = None

    document_id: int | None = None

    extraction_schema: dict | None = None

    question: str

    limit: int = 5

    debug: bool = False


class CitationResponse(BaseModel):

    document_id: int

    document_name: str

    chunk_index: int

    similarity_score: float


class RetrievedChunkResponse(BaseModel):

    document_name: str

    chunk_index: int

    similarity_score: float

    content: str


class DebugResponse(BaseModel):

    prompt: str

    retrieved_chunks: list[RetrievedChunkResponse]

    rewritten_query: str


class ChatResponse(BaseModel):

    conversation_id: int

    answer: str

    citations: list[CitationResponse]

    debug: DebugResponse | None = None
