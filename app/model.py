import subprocess
import json

def generate_answer(question, chunks):
    prompt = f"""
Answer the question using the following context:

{'\n\n'.join(chunks)}

Question: {question}
Answer:
"""
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
    )
    response = result.stdout.decode()
    # Extract links manually if needed
    return response.strip(), []
