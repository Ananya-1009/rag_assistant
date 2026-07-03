def build_prompt(query: str, results: dict) -> str:
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    context = ""

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

    Answer ONLY using the retrieved context below.

    Rules:

    1. Never use your own knowledge.

    2. The retrieved context may contain chunks from multiple documents.

    3. Before answering, identify which document(s) are relevant to the user's question.

    4. Ignore chunks from unrelated documents.

    5. Never combine information from different people or documents unless the user explicitly asks to compare or summarize multiple documents.

    6. If information is missing, say:
    "I couldn't find that information in the uploaded documents."

    7. For "Who is..." questions, give a short descriptive answer instead of only returning the person's name.

    8. Be concise but complete.

    --------------------------------------------------

    Retrieved Context:

    {context}

    --------------------------------------------------

    Question:

    {query}

    Answer:
    """
    print("=" * 80)
    print("PROMPT SENT TO LLM")
    print(prompt)
    print("=" * 80)
    return prompt