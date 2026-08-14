from docx import Document

from pathlib import Path

from app.document_processing.extractors.base import (
    BaseDocumentExtractor,
)


class DocxExtractor(
    BaseDocumentExtractor,
):

    def extract(
        self,
        file_path: Path,
    ) -> str:

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )