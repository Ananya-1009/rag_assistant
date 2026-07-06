from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import UploadFile,File
from datetime import datetime
from services.rag_service import ask_question
from database.db import initialize_database
from database.chat_repository import create_chat,get_all_chats,get_chat
from database.chat_repository import get_chat, update_chat_title
from utils.chat_title import generate_title
import json
from database.chat_repository import (get_chat,update_chat_title)
from utils.chat_title import generate_title
from database.message_repository import add_message,get_messages
from database.document_repository import add_document,get_documents
from fastapi.responses import StreamingResponse
from llm.ollama_client import stream_response
from services.rag_service import prepare_question
from storage.chat_manager import chat_manager
from config import ALLOWED_EXTENSIONS,MAX_UPLOAD_SIZE,UPLOAD_FOLDER
from storage.chat_manager import chat_manager
from logger import logger
from extractors.extractor_dispatcher import extract_document
import shutil
import re
from pathlib import Path
from chunking.text_chunker import chunk_text
from services.document_processor import process_document
from services.search_service import search_documents
from pydantic import BaseModel
class SearchRequest(BaseModel):
    query:str
class ChatRequest(BaseModel):
    question:str
class RenameChatRequest(BaseModel):
    title: str
def secure_filename(filename:str)->str:
    filename=Path(filename).name
    filename=filename.replace(" ","_")
    filename = re.sub(r'[^A-Za-z0-9._-]', '', filename)
    return filename
def generate_unique_filename(filename:str)->str:
    path=Path(filename)
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{path.stem}_{timestamp}{path.suffix}"
app=FastAPI(title="Local RAG Assistant")
initialize_database()
if len(get_all_chats())==0:
    create_chat("Chat 1")
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

@app.get("/", response_class=HTMLResponse)
async def home():
    template = templates.get_template("index.html")

    html = template.render()

    return HTMLResponse(content=html)
@app.post("/upload")
async def upload_file(file: UploadFile=File(...)):
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    extension=Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        logger.warning(f"Rejected upload: {file.filename}")
        return{
            "success":False,
            "filename": None,
            "message":f"'{extension}' files are not allowed."
        }
    file.file.seek(0,2)
    file_size=file.file.tell()
    file.file.seek(0)
    if file_size>MAX_UPLOAD_SIZE:
        logger.warning(f"Rejected upload: {file.filename}")
        
        return{
            "success":False,
            "filename": None,
            "message":"File exceeds the 25 MB upload limit."
        }
    safe_name = secure_filename(file.filename)
    unique_name = generate_unique_filename(safe_name)
    destination=UPLOAD_FOLDER/unique_name
    
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    logger.info(f"Uploaded: {unique_name}")
    chat_id = chat_manager.get_chat_id()
    print(f"Current Chat: {chat_id}")
    chunks,embeddings=process_document(destination)
    document_id=chunks[0]["document_id"]
    add_document(chat_id,document_id,unique_name)
    logger.info(f"Chunks created: {len(chunks)}")
    
    return{
        "success": True,
        "filename": unique_name,
        "chunks": len(chunks),
        "message":"Document processed successfully."
    }
@app.post("/search")
async def search(request:SearchRequest):
    results=search_documents(request.query)
    return results
@app.post("/chat")
async def chat(request:ChatRequest):
    chat_id=chat_manager.get_chat_id()
    if chat["title"].startswith("Chat"):
        title=generate_title(request.question)
        update_chat_title(chat_id,title)
    add_message(chat_id,"user",request.question)
    result=ask_question(request.question)
    add_message(chat_id,"assistant",result["answer"])
    return result
@app.post("/chat_stream")
async def chat_stream(request:ChatRequest):
    chat_id=chat_manager.get_chat_id()
    chat = get_chat(chat_id)
    if chat["title"].startswith("Chat"):
        title = generate_title(request.question)
        update_chat_title(chat_id, title)
    add_message(chat_id,"user",request.question)
    prompt,results=prepare_question(request.question)
    sources=[]
    metadatas=results.get("metadatas",[])
    if metadatas:
        for metadata in metadatas[0]:
            sources.append(metadata["filename"])
    async def generate():
        full_answer=""
        for token in stream_response(prompt):
            full_answer+=token
            yield json.dumps({
                "type":"token",
                "content":token
            })+"\n"
        add_message(chat_id,"assistant",full_answer)
        filenames=[]
        seen=set()
        for metadata in results["metadatas"][0]:
            filename=metadata["filename"]
            if filename not in seen:
                filenames.append(filename)
                seen.add(filename)
        
        yield json.dumps({
            "type": "sources",
            "data": filenames
        }) + "\n"
    return StreamingResponse(generate(),media_type="application/x-ndjson")
@app.post("/new_chat")
async def new_chat():
    chats=get_all_chats()
    title=f"Chat {len(chats)+1}"
    chat_id=create_chat(title)
    chat_manager.set_chat(chat_id)
    return{
        "chat_id":chat_id,
        "title":title
    }
@app.get("/chats")
async def get_chats():
    chats=get_all_chats()
    return [
        {
            "id":chat["id"],
            "title":chat["title"]
        }
        for chat in chats
    ]
@app.post("/switch_chat/{chat_id}")
async def switch_chat(chat_id:str):
    chat=get_chat(chat_id)
    if chat is None:
        return{
            "success":False
        }
    chat_manager.set_chat(chat_id)
    return{
        "success":True
    }
@app.get("/documents")
async def documents():
    chat_id=chat_manager.get_chat_id()
    docs=get_documents(chat_id)
    return [
        {
            "filename":doc["filename"],
            "document_id":doc["document_id"]
        }
        for doc in docs
    ]
@app.get("/messages")
async def get_chat_messages():
    chat_id=chat_manager.get_chat_id()
    messages=get_messages(chat_id)
    return [
        {
            "role":message["role"],
            "message":message["message"]
        }
        for message in messages
    ]
@app.put("/chats/{chat_id}")
async def rename_chat(chat_id: str, request: RenameChatRequest):
    update_chat_title(chat_id, request.title)
    return {"success": True}