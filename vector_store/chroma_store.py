import chromadb
from config import CHROMA_DB_PATH
class ChromaStore:
    COLLECTION_NAME="documents"
    def __init__(self):
        self.client=chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
        self.chunk_collection=self.client.get_or_create_collection(name="chunks")
        self.document_collection=self.client.get_or_create_collection(name="documents")
    def add_documents(self,chunks:list[dict],embeddings,chat_id):
        print(">>> ENTERED add_documents")
        ids=[]
        documents=[]
        metadatas=[]
        for chunk in chunks:
            ids.append(f"{chunk['document_id']}_{chunk['chunk_id']}")
            documents.append(chunk["text"])
            metadatas.append(
                {
                    "chat_id": chat_id,
                    "document_id":chunk["document_id"],
                    "filename":chunk["filename"],
                    "filetype":chunk["filetype"],
                    "chunk_id":chunk["chunk_id"],
                }
            )
        print("IDs:", len(ids))
        print("Documents:", len(documents))
        print("Metadatas:", len(metadatas))
        print("Embeddings type:", type(embeddings))
        print("Embeddings length:", len(embeddings))
        self.chunk_collection.add(ids=ids,documents=documents,embeddings=embeddings.tolist(),metadatas=metadatas,)
    def get_all_documents(self):
        return self.chunk_collection.get(include=["metadatas"])
    def count(self):
        return self.chunk_collection.count()
    def search(self,query_embedding,n_results: int=5,document_ids=None,chat_id=None):
        query={
            "query_embeddings":[query_embedding.tolist()],
            "n_results":n_results
        }
        where={}
        if chat_id is not None:
            where["chat_id"]=chat_id
        if document_ids is not None:
            where["document_id"]={"$in":document_ids}
        if where:
            query["where"] = where
        print(query)
        print(">>> About to call Chroma add()")
        results=self.chunk_collection.query(**query)

        return results
    def add_document_embedding(self,document_id,filename,embedding,):
        self.document_collection.add(
            ids=[document_id],
            documents=[filename],
            embeddings=[embedding.tolist()],
            metadatas=[
                {
                    "document_id":document_id,
                    "filename":filename,
                }
            ]
        )
    def search_documents(self,query_embedding,top_k=2,):
        return self.document_collection.query(query_embeddings=[query_embedding.tolist()],n_results=top_k,include=["metadatas","distances"])
    def count_documents(self):
        return self.document_collection.count()
    def get_all_document_embeddings(self):
        return self.document_collection.get(
            include=["documents", "metadatas"]
        )
    def delete_chat(self, chat_id):
        self.chunk_collection.delete(where={"chat_id": chat_id})