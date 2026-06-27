import csv
from pathlib import Path
def extract_csv(file_path:Path)->str:
    text=[]
    with file_path.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:
        reader=csv.reader(file)
        for row in reader:
            values=[
                str(cell).strip()
                for cell in row
            ]
            text.append(" | ".join(values))
    return "\n".join(text).strip()