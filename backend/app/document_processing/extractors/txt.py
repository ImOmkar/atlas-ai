from pathlib import Path

from app.document_processing.extractors.base import (
    BaseDocumentExtractor,
)


class TextExtractor(BaseDocumentExtractor):

    def extract(
        self,
        file_path: Path,
    ) -> str:

        return file_path.read_text(
            encoding="utf-8",
        )