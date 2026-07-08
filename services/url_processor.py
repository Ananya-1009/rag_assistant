import requests
from bs4 import BeautifulSoup
def extract_text_from_url(url:str):
    response=requests.get(url,timeout=10,headers={"User-Agent":"Mozilla/5.0"})
    response.raise_for_status()
    soup=BeautifulSoup(response.text,"html.parser")
    title = soup.title.string.strip() if soup.title else url
    for tag in soup([
        "script",
        "style",
        "noscript"
    ]):
        tag.decompose()
    text=soup.get_text(separator="\n")
    lines=[
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]
    return title,"\n".join(lines)