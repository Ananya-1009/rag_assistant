import logging
from config import LOG_FOLDER
LOG_FOLDER.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_FOLDER/"rag.log",
    level=logging.INFO,
    format="%(asctime)s|%(levelname)s|%(message)s"
)
logger=logging.getLogger("rag_assistant")