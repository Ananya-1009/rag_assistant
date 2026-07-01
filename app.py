from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import UploadFile,File
from datetime import datetime
from services.rag_service import ask_question
from config import ALLOWED_EXTENSIONS,MAX_UPLOAD_SIZE,UPLOAD_FOLDER
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
    chunks,embeddings=process_document(destination)
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
    return ask_question(request.question)
