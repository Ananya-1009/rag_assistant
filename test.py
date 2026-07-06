from llm.ollama_client import stream_response

for token in stream_response("Tell me about Python."):
    print(token, end="", flush=True)