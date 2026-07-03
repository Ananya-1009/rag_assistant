from sentence_transformers import CrossEncoder
model=CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query,results,top_k=6):
    documents=results["documents"][0]
    metadatas=results["metadatas"][0]
    distances=results["distances"][0]
    pairs=[(query,document) for document in documents]
    scores=model.predict(pairs)
    ranked = sorted(
        zip(scores, documents, metadatas, distances),
        key=lambda x: x[0],
        reverse=True
    )
    ranked=ranked[:top_k]
    return {
        "documents": [[x[1] for x in ranked]],
        "metadatas": [[x[2] for x in ranked]],
        "distances": [[x[3] for x in ranked]],
    }