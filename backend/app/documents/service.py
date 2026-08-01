from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import BackgroundTasks, UploadFile

from app.projects.exceptions import ProjectNotFoundError
from app.documents.models import Document
from app.documents.enums import DocumentStatus
from app.projects.repository import ProjectRepository
from app.documents.repository import DocumentRepository
from app.documents.exceptions import DocumentFileNotFoundError, DocumentNotFoundError

from pathlib import Path

from app.db.session import SessionLocal

from app.document_processing.service import (
    DocumentProcessingService,
)

UPLOAD_DIRECTORY = Path("storage/documents")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


class DocumentService:

    def __init__(self, db):
        self.project_repository = ProjectRepository(db)
        self.document_repository = DocumentRepository(db)

    def get_all(
        self,
        organization_id: int,
        project_id: int,
    ) -> list[Document]:

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        return self.document_repository.get_all(
            project_id,
        )

    def get_by_id(
        self,
        organization_id: int,
        project_id: int,
        document_id: int,
    ) -> Document:

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        document = self.document_repository.get_by_id(
            project_id,
            document_id,
        )

        if document is None:
            raise DocumentNotFoundError()

        return document

    def upload(
        self,
        organization_id: int,
        project_id: int,
        file: UploadFile,
        background_tasks: BackgroundTasks
    ):

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        extension = Path(file.filename).suffix

        filename = f"{uuid4()}{extension}"

        storage_path = (
            UPLOAD_DIRECTORY / filename
        )

        with storage_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )


        document = Document(
            project_id=project.id,
            filename=filename,
            original_filename=file.filename,
            content_type=file.content_type,
            file_size=storage_path.stat().st_size,
            storage_path=str(storage_path),
            status=DocumentStatus.PROCESSING,
        )

        document = self.document_repository.create(
            document,
        )

        background_tasks.add_task(
            self._process_document,
            document.id,
        )

        return document


    def _process_document(
        self,
        document_id: int,
    ):
        db = SessionLocal()

        try:
            service = DocumentProcessingService(
                db,
            )

            service.process_document(
                document_id,
            )

        finally:
            db.close()


    def download(
        self,
        organization_id: int,
        project_id: int,
        document_id: int,
    ) -> Document:

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        document = self.document_repository.get_by_id(
            project_id,
            document_id,
        )

        if document is None:
            raise DocumentNotFoundError()

        path = Path(document.storage_path)

        if not path.exists():
            raise DocumentFileNotFoundError()

        return document


    def delete(
        self,
        organization_id: int,
        project_id: int,
        document_id: int,
    ) -> None:

        project = self.project_repository.get_by_id(
            organization_id,
            project_id,
        )

        if project is None:
            raise ProjectNotFoundError()

        document = self.document_repository.get_by_id(
            project_id,
            document_id,
        )

        if document is None:
            raise DocumentNotFoundError()

        path = Path(document.storage_path)

        if path.exists():
            path.unlink()

        self.document_repository.delete(
            document,
        )