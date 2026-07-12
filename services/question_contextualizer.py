from llm.ollama_client import generate_response
def contextualize_question(question, conversation_history):
    if not conversation_history:
        return question

    history = ""

    for message in conversation_history[-6:]:
        history += f"{message['role']}: {message['message']}\n"

    prompt = f"""
Rewrite the current question as a standalone question using the
conversation history only to resolve references such as he, she, it,
they, this, or that.

Do not answer the question.
Do not add new facts.
If the question is already standalone, return it unchanged.

Conversation History:
{history}

Current Question:
{question}

Standalone Question:
"""

    return generate_response(prompt).strip()