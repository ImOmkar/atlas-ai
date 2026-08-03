from sqlalchemy.orm import (
    Session,
)

from sqlalchemy import or_

from app.projects.models import (
    Project,
)

from app.documents.models import (
    Document,
)

from app.document_chunks.models import (
    DocumentChunk,
)



class KeywordSearchRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def search(
        self,
        organization_id: int,
        project_id: int,
        query: str,
        limit: int = 10,
    ) -> list[DocumentChunk]:


        return (
            self.db.query(
                DocumentChunk,
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .join(
                Project,
                Project.id == Document.project_id,
            )
            .filter(
                Project.organization_id == organization_id,
                Project.id == project_id,
                DocumentChunk.content.ilike(
                    f"%{query}%"
                ),
            )
            .limit(limit)
            .all()
        )




# if __name__ == "__main__":

#     from app.db.session import SessionLocal

#     db = SessionLocal()

#     repository = KeywordSearchRepository(
#         db,
#     )

#     results = repository.search(
#         organization_id=1,
#         project_id=1,
#         query="LEAVE POLICY",
#     )

#     for chunk in results:
#         print("=" * 80)
#         print(chunk.chunk_index)
#         print(chunk.content)

#     db.close()