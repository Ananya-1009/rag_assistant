from embeddings.embedding_model import generate_embedding
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from vector_store.chroma_store import ChromaStore
store=ChromaStore()
def ask_question(question:str):
    query_embedding=generate_embedding(question)
    results=store.search(
        query_embedding=query_embedding,
        n_results=5
    )
    prompt=build_prompt(question,results)
    answer=generate_response(prompt)
    sources=[]
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