from app.document_processing.extractors.pdf import PdfExtractor

from app.document_processing.extractors.docx import DocxExtractor

from app.document_processing.extractors.txt import TextExtractor


EXTRACTORS = {
    ".pdf": PdfExtractor(),
    ".docx": DocxExtractor(),
    ".txt": TextExtractor(),
}