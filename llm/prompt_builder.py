def build_prompt(query: str, results: dict,conversation_history: list = None) -> str:
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    context = ""
    # history = ""

    # if conversation_history:
    #     history = "Conversation History:\n\n"

    #     for message in conversation_history:
    #         role = message["role"].capitalize()
    #         history += f"{role}: {message['message']}\n\n"
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

    # Use the conversation history to understand references
    # such as "he", "she", "it", "that", or follow-up questions.

    Use ONLY the retrieved context to answer factual questions
    about the uploaded documents.

    If the user asks about the conversation itself
    (for example "What was my first question?"
    or "Summarize our conversation"),
    answer using the conversation history.

    Rules:

    1. You MUST answer only from the Retrieved Context.

    2. Never answer using your own knowledge.

    3. Never guess or infer facts that are not explicitly present.

    4. If the Retrieved Context is empty or does not contain the answer, reply exactly:

    "I couldn't find that information in the uploaded documents."

    5. Do not use world knowledge, even if you know the answer."

    6. Begin directly with the answer. Do NOT say:
    - "According to the retrieved context..."
    - "Based on the uploaded documents..."
    - "I will refer to..."

    7. Format your answer using Markdown:
    - Use ## for main headings.
    - Use ### for subheadings.
    - Use bullet points (-) for lists.
    - Use numbered lists when describing steps.
    - Use **bold** for important terms.

    8. For definitions, start with a one- or two-sentence definition, then explain in sections.

    9. Keep the answer concise, avoid repetition, and preserve important technical details.
    10. Do NOT include sources, filenames, document names, or chunk numbers in your answer.
    The application will display the sources separately.
   --------------------------------------------------

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