from pathlib import Path
from extractors.extractor_dispatcher import extract_document
from chunking.text_chunker import chunk_text
from embeddings.embedding_model import generate_embeddings
import uuid
def process_document(file_path:Path)->list[dict]:
    document_id = str(uuid.uuid4())
    text=extract_document(file_path)
    chunks=chunk_text(text=text,file_path=file_path,document_id=document_id)
    embeddings=generate_embeddings(chunks)
    store = ChromaStore()
    store.add_documents(
        chunks,
        embeddings
    )
    return chunks,embeddings