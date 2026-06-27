from pathlib import Path
from extractors.pdf_extractor import extract_pdf
from extractors.txt_extractor import extract_txt
from extractors.excel_extractor import extract_excel
from extractors.docx_extractor import extract_docx
from extractors.csv_extractor import extract_csv
EXTRACTORS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".txt": extract_txt,
    ".xlsx": extract_excel,
    ".csv": extract_csv,
}
def extract_document(file_path:Path)->str:
    extension=file_path.suffix.lower()
    extractor=EXTRACTORS.get(extension)
    if extractor is None:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )
    return extractor(file_path)