from app.documents.models import Document


class DocumentRepository:

    def __init__(self, db):
        self.db = db

    def get_all(
        self,
        project_id: int,
    ) -> list[Document]:
        return (
            self.db.query(Document)
            .filter(
                Document.project_id == project_id,
            )
            .order_by(
                Document.created_at.desc(),
            )
            .all()
        )


    def get_by_id(
        self,
        project_id: int,
        document_id: int,
    ) -> Document | None:
        return (
            self.db.query(Document)
            .filter(
                Document.id == document_id,
                Document.project_id == project_id,
            )
            .first()
        )


    def get_by_id_(
        self,
        document_id: int,
    ) -> Document | None:

        return (
            self.db.query(Document)
            .filter(
                Document.id == document_id,
            )
            .first()
        )

    def create(
        self,
        document: Document,
    ) -> Document:

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document


    def delete(
        self,
        document: Document,
    ) -> None:

        self.db.delete(document)
        self.db.commit()


    def update(
        self,
        document: Document,
    ) -> Document:

        self.db.commit()
        self.db.refresh(document)

        return document