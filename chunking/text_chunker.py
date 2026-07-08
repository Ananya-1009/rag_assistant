from pathlib import Path
from config import CHUNK_SIZE,CHUNK_OVERLAP
def create_chunk(chunk_id:int,text:str,filename:str,filetype:str,document_id:str)->dict:
    return {
        "chunk_id": chunk_id,
        "filename": filename,
        "filetype": filetype,
        "text": text,
        "document_id": document_id,
    }
def find_split_position(text:str,start:int,end:int)->int:
    paragraph=text.rfind("\n\n",start,end)
    if paragraph!=-1:
        return paragraph+2
    for seperator in [". ","! ","? "]:
        sentence=text.rfind(seperator,start,end)
        if sentence!=-1:
            return sentence+len(seperator)
    space=text.rfind(" ",start,end)
    if space!=-1:
        return space
    return end
def chunk_text(text:str,filename:str,filetype:str,document_id:str)->list[dict]:
    chunks=[]
    chunk_id=1
    for start in range(0,len(text),CHUNK_SIZE):
        end=min(start+CHUNK_SIZE,len(text))
        if end<len(text):
            end=find_split_position(text,start,end)
        chunk=text[start:end].strip()
        chunks.append(
            create_chunk(
                chunk_id=chunk_id,
                text=chunk,
                filename=filename,
                filetype=filetype,
                document_id=document_id
            )
        )
        start = max(end-CHUNK_OVERLAP,start+1)
        chunk_id+=1;
    return chunks