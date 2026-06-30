from sentence_transformers import SentenceTransformer
MODEL_NAME="all-MiniLM-L6-v2"
model=SentenceTransformer(MODEL_NAME)
def generate_embedding(text:str):
    return model.encode(text)
def generate_embeddings(chunks:list[dict]):
    texts=[
        chunk["text"]
        for chunk in chunks
    ]
    embeddings=model.encode(texts)
    return embeddings