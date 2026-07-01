from vector_store.chroma_store import ChromaStore

store = ChromaStore()

results = store.get_all_documents()

print(results["metadatas"])