from pathlib import Path
def extract_txt(file_path:Path)->str:
    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        text=file.read()
    return text