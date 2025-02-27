# llama_integration.py
import ollama
import asyncio
MODEL_NAME = "llama3"
async def generate_summary(content: str) -> str:
    prompt = f"Please summarize the following book content:\n\n{content}"
    response = await asyncio.to_thread(ollama.generate, model=MODEL_NAME, prompt=prompt)
    return response['response']
