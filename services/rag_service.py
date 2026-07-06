from embeddings.embedding_model import generate_embedding
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from vector_store.chroma_store import ChromaStore
from services.retrieval_service import retrieve_documents
from storage.chat_manager import chat_manager
from database.message_repository import get_messages
store=ChromaStore()
def ask_question(question:str):
    prompt,results=prepare_question(question)
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
def prepare_question(question:str):
    query_embedding=generate_embedding(question)
    results=retrieve_documents(question,query_embedding)
    chat_id=chat_manager.get_chat_id()
    history=get_messages(chat_id)[-11:-1]
    prompt=build_prompt(question,results,history)
    return prompt,results