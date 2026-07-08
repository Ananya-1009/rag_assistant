from services.url_processor import extract_text_from_url

print(
    extract_text_from_url(
        "https://fastapi.tiangolo.com/"
    )[:1000]
)