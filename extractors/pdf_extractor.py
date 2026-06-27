import fitz
from pathlib import Path
def extract_pdf(file_path:Path)->str:
    document=fitz.open(file_path)
    text=""
    for page in document:
        text+=page.get_text()
    document.close()
    return text.strip()