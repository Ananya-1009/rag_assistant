from vector_store.chroma_store import ChromaStore
from collections import defaultdict
store=ChromaStore()
def retrieve_documents(question,query_embedding,n_results=30):
    document_scores = defaultdict(float)

    results = store.search(query_embedding=query_embedding,n_results=n_results)
    print("=" * 60)
    print("INITIAL CHUNK RETRIEVAL")

    for metadata in results["metadatas"][0]:
        print(metadata["filename"])

    print("=" * 60)
    metadatas=results["metadatas"][0]
    distances=results["distances"][0]
    for metadata, distance in zip(metadatas, distances):
        document_id = metadata["document_id"]

        document_scores[document_id] += (
            1 / (distance + 0.001)
        )
    sorted_documents = sorted(
        document_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    best_score=sorted_documents[0][1]
    selected_document_ids = []
    THRESHOLD = 0.85
    for document_id, score in sorted_documents:
        ratio = score / best_score
        if ratio >= THRESHOLD:
            selected_document_ids.append(document_id)
    print("=" * 60)
    print("SELECTED DOCUMENTS")

    for document_id in selected_document_ids:
        print(document_id)
    print("DOCUMENT SCORES")
    for document_id, score in sorted_documents:
        print(document_id, score)

    print("=" * 60)
    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []
    for metadata, document, distance in zip(
        results["metadatas"][0],
        results["documents"][0],
        results["distances"][0]
    ):
        if metadata["document_id"] in selected_document_ids:
            filtered_documents.append(document)
            filtered_metadatas.append(metadata)
            filtered_distances.append(distance)
    filtered_results = {
    "documents": [filtered_documents],
    "metadatas": [filtered_metadatas],
    "distances": [filtered_distances]
    }

    print("=" * 60)
    print("FINAL CONTEXT")

    for metadata, document in zip(
        filtered_results["metadatas"][0],
        filtered_results["documents"][0]
    ):
        print("-" * 40)
        print(metadata["filename"])
        print(f"Chunk {metadata['chunk_id']}")
        print(document)

    print("=" * 60)
    return filtered_results