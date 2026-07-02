from document_store.document_index import document_index
from embeddings.embedding_model import generate_embedding

document_index.add_document(
    document_id="doc1",
    filename="Operating Systems.pdf",
    embedding=generate_embedding(
        "Deadlock, semaphore, process scheduling, CPU scheduling"
    )
)

document_index.add_document(
    document_id="doc2",
    filename="Machine Learning.pdf",
    embedding=generate_embedding(
        "Neural networks, CNN, RNN, gradient descent"
    )
)

document_index.add_document(
    document_id="doc3",
    filename="DBMS.pdf",
    embedding=generate_embedding(
        "Normalization, SQL, transactions, indexing"
    )
)

query = "Explain deadlock"

query_embedding = generate_embedding(query)

results = document_index.search_documents(query_embedding)

print(results)