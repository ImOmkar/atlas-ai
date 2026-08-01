from pathlib import Path

import pytesseract

from pdf2image import convert_from_path

from app.document_processing.ocr.base import (
    BaseOCREngine,
)

from app.document_processing.ocr.config import (
    POPPLER_PATH,
)

from app.document_processing.ocr.base import (
    BaseOCREngine,
)


class TesseractOCREngine(
    BaseOCREngine,
):

    def extract(
        self,
        file_path: Path,
    ) -> str:

        pages = convert_from_path(
            file_path,
            poppler_path=str(
                POPPLER_PATH,
            ),
        )

        extracted_text = []

        for page in pages:

            text = pytesseract.image_to_string(
                page,
            )

            extracted_text.append(
                text,
            )

        return "\n".join(
            extracted_text,
        )