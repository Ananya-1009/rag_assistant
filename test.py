from vector_store.chroma_store import ChromaStore

store = ChromaStore()

results = store.get_all_documents()

for metadata in results["metadatas"]:
    print(metadata["filename"])