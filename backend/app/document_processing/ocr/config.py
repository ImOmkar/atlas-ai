from pathlib import Path

import pytesseract

POPPLER_PATH = Path(
    r"F:\OmkarParab\poppler-26.02.0\Library\bin"
)

print(POPPLER_PATH.exists())

print((POPPLER_PATH / "pdfinfo.exe").exists())

print((POPPLER_PATH / "pdftoppm.exe").exists())


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)