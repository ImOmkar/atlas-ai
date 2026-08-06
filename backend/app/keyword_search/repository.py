from sqlalchemy.orm import (
    Session,
)


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

    def get_chunks(
        self,
        organization_id: int,
        project_id: int,
    ) -> list[DocumentChunk]:

        return (
            self.db.query(
                DocumentChunk,
                Document,
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
            )
            .order_by(
                DocumentChunk.id,
            )
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