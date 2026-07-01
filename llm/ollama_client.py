from ollama import Client
MODEL_NAME="llama3.2:3b"
client=Client(host="http://localhost:11434")
def generate_response(prompt:str)->str:
    response=client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    return response["message"]["content"]
