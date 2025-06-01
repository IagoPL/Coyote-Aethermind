import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_answer_openrouter(question: str, context_chunks: list[str], model: str = "openai/gpt-3.5-turbo") -> str:
    """
    Uses OpenRouter to generate a natural language answer from provided context.

    Args:
        question (str): The user's question.
        context_chunks (list[str]): Relevant text chunks from rule index.
        model (str): Model to use (default: GPT-3.5 Turbo)

    Returns:
        str: The generated answer from the model.
    """
    prompt = f"""Eres un juez profesional de Magic: The Gathering. Usa el contexto para dar una respuesta específica, incluso si el término exacto no aparece.


### Contexto:
{chr(10).join(context_chunks)}

### Pregunta:
{question}

### Respuesta:"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://tu-dominio.dev",
        "X-Title": "Coyote-Aethermind"
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
