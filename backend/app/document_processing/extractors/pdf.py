import fitz

from pathlib import Path

from app.document_processing.extractors.base import (
    BaseDocumentExtractor,
)



class PdfExtractor(
    BaseDocumentExtractor,
):

    def extract(
        self,
        file_path: Path,
    ) -> str:

        text = []

        document = fitz.open(file_path)

        for page in document:
            text.append(
                page.get_text()
            )

        document.close()

        return "\n".join(text)