from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app=FastAPI(title="Local RAG Assistant")
# app.mount("/static",StaticFiles(directory="static"),name="static")
# templates=Jinja2Templates(directory="templates")
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
# @app.get("/")
# async def home(request:Request):
#     return templates.TemplateResponse(
#         "index.html",
#         {"request":request}
#     )
# @app.get("/")
# async def home(request: Request):
#     template = templates.get_template("index.html")
#     return {"status": "template found"}
# @app.get("/")
# async def home():
#     return {"status": "FastAPI is working"}
@app.get("/", response_class=HTMLResponse)
async def home():
    template = templates.get_template("index.html")

    html = template.render()

    return HTMLResponse(content=html)