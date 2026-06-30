from embeddings.embedding_model import generate_embedding
from vector_store.chroma_store import ChromaStore
store=ChromaStore()
def search_documents(query:str,n_results:int=5):
    query_embedding=generate_embedding(query)
    results=store.search(query_embedding=query_embedding,n_results=n_results,)
    return results