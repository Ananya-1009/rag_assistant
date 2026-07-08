from pathlib import Path
from extractors.extractor_dispatcher import extract_document
from chunking.text_chunker import chunk_text
from embeddings.embedding_model import generate_embeddings,generate_embedding
from vector_store.chroma_store import ChromaStore
import uuid
import numpy as np
from document_store.document_index import document_index
from storage.chat_manager import chat_manager
def process_document(file_path:Path)->list[dict]:
    document_id = str(uuid.uuid4())
    text=extract_document(file_path)
    chunks=chunk_text(text=text,filename=file_path.name, filetype=file_path.suffix.lower(),document_id=document_id)
    embeddings=generate_embeddings(chunks)
    document_embedding = np.mean(embeddings,axis=0)
    document_index.add_document(document_id=document_id,filename=file_path.name,embedding=document_embedding)
    store = ChromaStore()
    chat_id = chat_manager.get_chat_id()
    store.add_documents(
        chunks,
        embeddings,
        chat_id
    )
    store.add_document_embedding(document_id,file_path.name,document_embedding,)
    print(store.get_all_document_embeddings())
    print(document_index.get_documents())
    print("Chunk count:", store.count())
    print("Document count:", store.count_documents())
    return chunks,embeddings