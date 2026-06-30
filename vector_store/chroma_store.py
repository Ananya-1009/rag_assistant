import chromadb
from config import CHROMA_DB_PATH
class ChromaStore:
    COLLECTION_NAME="documents"
    def __init__(self):
        self.client=chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
        self.collection=self.client.get_or_create_collection(name=self.COLLECTION_NAME)
    def add_documents(self,chunks:list[dict],embeddings,):
        ids=[]
        documents=[]
        metadatas=[]
        for chunk in chunks:
            ids.append(f"{chunk['document_id']}_{chunk['chunk_id']}")
            documents.append(chunk["text"])
            metadatas.append(
                {
                    "document_id":chunk["document_id"],
                    "filename":chunk["filename"],
                    "filetype":chunk["filetype"],
                    "chunk_id":chunk["chunk_id"],
                }
            )
        self.collection.add(ids=ids,documents=documents,embeddings=embeddings.tolist(),metadatas=metadatas,)
    def get_all_documents(self):
        return self.collection.get()
    def count(self):
        return self.collection.count()
    def search(self,query_embedding,n_results: int=5,):
        results=self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
        )
        return results