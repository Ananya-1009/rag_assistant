from uuid import uuid4
from services.url_processor import extract_text_from_url
from chunking.text_chunker import chunk_text
from embeddings.embedding_model import generate_embeddings
def process_url(url:str):
    title,text=extract_text_from_url(url)
    document_id=str(uuid4())
    chunks = chunk_text(text=text,filename=title,filetype="url",document_id=document_id)
    embeddings=generate_embeddings(chunks)
    return document_id,title,chunks,embeddings