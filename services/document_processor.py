from pathlib import Path
from extractors.extractor_dispatcher import extract_document
from chunking.text_chunker import chunk_text
def process_document(file_path:Path)->list[dict]:
    text=extract_document(file_path)
    chunks=chunk_text(text=text,file_path=file_path)
    return chunks