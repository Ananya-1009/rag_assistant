from vector_store.chroma_store import ChromaStore
from retrieval.reranker import rerank
store = ChromaStore()
def retrieve_documents(question, query_embedding, n_results=20):
    results=store.search(query_embedding=query_embedding,n_results=n_results)
    results=rerank(question,results,top_k=6)
    print("=" * 60)
    print("AFTER RERANKING")
    for metadata in results["metadatas"][0]:
        print(metadata["filename"], metadata["chunk_id"])
    print("=" * 60)
    return results