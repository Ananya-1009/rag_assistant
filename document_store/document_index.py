import numpy as np
class DocumentIndex:
    def cosine_similarity(self,embedding1,embedding2):
        embedding1=np.array(embedding1)
        embedding2=np.array(embedding2)
        return np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )
    def __init__(self):
        self.documents={}
    def add_document(self,document_id,filename,embedding,metadata=None):
        if metadata is None:
            metadata={}
        self.documents[document_id]={
            "document_id": document_id,
            "filename":filename,
            "embedding":embedding,
            "metadata":metadata
        }
    def get_documents(self):
        return self.documents
    def search_documents(self,query_embedding,top_k=2):
        scores=[]
        for document in self.documents.values():
            similarity=self.cosine_similarity(query_embedding,document["embedding"])
            scores.append({
                "document_id":document["document_id"],
                "filename":document["filename"],
                "score":similarity
            })
        scores.sort(key=lambda x:x["score"],reverse=True)
        return scores[:top_k]
document_index = DocumentIndex()
