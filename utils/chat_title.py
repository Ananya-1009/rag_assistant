import re

STOP_WORDS = {
    "what",
    "who",
    "is",
    "are",
    "the",
    "a",
    "an",
    "tell",
    "me",
    "about",
    "please",
    "explain"
}


def generate_title(question: str):

    words = re.findall(r"[A-Za-z0-9]+", question)

    words = [
        word
        for word in words
        if word.lower() not in STOP_WORDS
    ]

    if not words:
        return "New Chat"

    return " ".join(words[:4]).title()