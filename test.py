from embeddings.embedding_model import generate_embedding
from vector_store.chroma_store import ChromaStore

store = ChromaStore()

query = "What is Artificial Intelligence?"

query_embedding = generate_embedding(query)

results = store.search(query_embedding)

print("Documents:")
print(results["documents"][0])

print()

print("Metadata:")
print(results["metadatas"][0])

print()

print("Distances:")
print(results["distances"][0])