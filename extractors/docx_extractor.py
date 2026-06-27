from pathlib import Path
from docx import Document
def extract_docx(file_path:Path)->str:
    document=Document(file_path)
    text=[]
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text.strip())
    return "\n".join(text)
