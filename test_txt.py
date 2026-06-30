from pathlib import Path

from chunking.text_chunker import chunk_text

text = (
    "Artificial Intelligence " * 100
)

chunks = chunk_text(
    text,
    Path("uploads/test_text.txt")
)

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print(chunk["chunk_id"])
    print(len(chunk["text"]))