def build_prompt(query: str, results: dict,conversation_history: list = None) -> str:
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    context = ""
    history = ""

    if conversation_history:
        history = "Conversation History:\n\n"

        for message in conversation_history:
            role = message["role"].capitalize()
            history += f"{role}: {message['message']}\n\n"
    if documents and metadatas:
        for metadata, document in zip(
            metadatas[0],
            documents[0]
        ):
            context += f"""
    ==================================================
    Document: {metadata["filename"]}
    Chunk: {metadata["chunk_id"]}

    {document}

    """

    prompt = f"""
    You are a Retrieval-Augmented Generation (RAG) assistant.

    Use the conversation history to understand references
    such as "he", "she", "it", "that", or follow-up questions.

    Use ONLY the retrieved context to answer factual questions
    about the uploaded documents.

    If the user asks about the conversation itself
    (for example "What was my first question?"
    or "Summarize our conversation"),
    answer using the conversation history.

    Rules:

    1. Never use information outside the retrieved context.

    2. The context may contain chunks from multiple documents. First identify the document(s) relevant to the question.

    3. Ignore unrelated documents and never mix information from different people unless the user explicitly asks for a comparison.

    4. If the answer is not available in the retrieved context, reply exactly:
    "I couldn't find that information in the uploaded documents."

    5. Begin directly with the answer. Do NOT say:
    - "According to the retrieved context..."
    - "Based on the uploaded documents..."
    - "I will refer to..."

    6. Format your answer using Markdown:
    - Use ## for main headings.
    - Use ### for subheadings.
    - Use bullet points (-) for lists.
    - Use numbered lists when describing steps.
    - Use **bold** for important terms.

    7. For definitions, start with a one- or two-sentence definition, then explain in sections.

    8. Keep the answer concise, avoid repetition, and preserve important technical details.
    9. Do NOT include sources, filenames, document names, or chunk numbers in your answer.
    The application will display the sources separately.
   --------------------------------------------------

    {history}

    --------------------------------------------------

    Retrieved Context:

    {context}

    --------------------------------------------------

    Current Question:

    {query}
    Answer:
    """
    print("=" * 80)
    print("PROMPT SENT TO LLM")
    print(prompt)
    print("=" * 80)
    return prompt