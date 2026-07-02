from embeddings.embedding_model import generate_embedding
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from vector_store.chroma_store import ChromaStore
from services.retrieval_service import retrieve_documents
store=ChromaStore()
def ask_question(question:str):
    query_embedding=generate_embedding(question)
    results=retrieve_documents(question,query_embedding)
    prompt=build_prompt(question,results)
    answer=generate_response(prompt)
    sources=[]
    print("Source files:")
    for metadata in results["metadatas"][0]:
        print(metadata["filename"])
    metadatas=results.get("metadatas",[])
    if metadatas and len(metadatas)>0:
        for metadata in metadatas[0]:
            sources.append(
                {
                    "filename":metadata["filename"],
                    "chunk_id":metadata["chunk_id"],
                }
            )

    return{
        "answer":answer,
        "sources":sources,
    }