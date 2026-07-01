def build_prompt(query:str,results:dict)->str:
    documents=results.get("documents",[])
    context=""
    if documents and len(documents)>0:
        context="\n\n".join(documents[0])
    prompt = f"""
You are a helpful AI assistant.
Answer the user's question ONLY using the context below.
If the answer is not present in the context, reply:
"I couldn't find that information in the uploaded documents."
--------------------
Context:
{context}
--------------------
Question:
{query}
Answer:
"""
    return prompt