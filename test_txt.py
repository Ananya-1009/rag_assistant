from pathlib import Path

from extractors.txt_extractor import extract_txt

text = extract_txt(
    Path("uploads/test_text.txt")
)

print(text)