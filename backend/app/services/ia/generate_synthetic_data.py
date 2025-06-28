"""
generate_synthetic_data.py

Generates synthetic QA examples for Aethermind AI training.

- Loads Magic rules chunks (FAISS embeddings).
- For each chunk, generates several questions.
- For each question, generates an answer using an LLM API.
- Saves the dataset in .jsonl format (compatible with Huggingface).

Usage:
    python -m app.services.ia.generate_synthetic_data
"""

import os
import json
import pickle
import time
import random
import requests

from app.config import CHUNKS_PATH, TRAINING_DATA_PATH, TRAINING_DATA_DIR
from app.services.ia import generate_synthetic_data_config as config

# --------------------------------------------------------------

def load_chunks():
    """
    Loads Magic rules chunks from pickle file.

    Returns:
        list[str]: List of text chunks.
    """
    print(f"USANDO CHUNKS_PATH: {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"✅ Cargados {len(chunks)} chunks.")
    return chunks

def call_llm_api(prompt):
    """
    Calls the LLM API to get a response.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The generated response.
    """
    headers = {
        "Content-Type": "application/json",
    }
    api_key = os.getenv("PUTER_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = {
        "messages": [
            {"role": "system", "content": "You are a Magic: The Gathering rules expert. Answer clearly and concisely."},
            {"role": "user", "content": prompt}
        ],
        "model": config.MODEL
    }

    try:
        response = requests.post(config.API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Puter format (adjust if needed)
        return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        print(f"⚠️ Error calling LLM API: {e}")
        return "Error generating answer."

def generate_question_prompts(chunk_text):
    """
    Generates prompts to create questions for a given chunk.

    Args:
        chunk_text (str): The chunk of Magic rules.

    Returns:
        list[str]: List of question prompts.
    """
    base_prompt = (
        f"""Eres un experto en reglas de Magic: The Gathering.

Voy a darte un fragmento de reglas. Quiero que generes {config.NUM_QUESTIONS_PER_CHUNK} preguntas que un jugador podría hacer basándose en este fragmento.

No repitas preguntas, deben ser variadas y reales (como las haría un jugador).

Fragmento de reglas:
\"\"\"
{chunk_text}
\"\"\"

Devuélveme SOLO la lista de preguntas, una por línea:
"""
    )
    return base_prompt

def save_dataset(dataset):
    """
    Saves the dataset in .jsonl format.

    Args:
        dataset (list[dict]): List of examples.
    """
    os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

    with open(TRAINING_DATA_PATH, "w", encoding="utf-8") as f:
        for entry in dataset:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

# --------------------------------------------------------------

def main():
    print("📚 Cargando chunks de reglas...")
    chunks = load_chunks()

    dataset = []
    total_questions_generated = 0

    print("🤖 Generando preguntas y respuestas sintéticas...")

    for idx, chunk in enumerate(chunks):
        print(f"\n🔹 Chunk {idx + 1}/{len(chunks)}")

        # Generar preguntas
        question_prompt = generate_question_prompts(chunk)
        questions_text = call_llm_api(question_prompt)

        questions = [q.strip("-• ") for q in questions_text.strip().split("\n") if q.strip()]
        questions = questions[:config.NUM_QUESTIONS_PER_CHUNK]

        print(f"📌 Preguntas generadas: {len(questions)}")

        for question in questions:
            print(f"  ❓ {question}")

            # Generar respuesta
            answer_prompt = (
                f"""Eres un experto en reglas de Magic: The Gathering.

Voy a darte una pregunta sobre las reglas y el fragmento de reglas correspondiente.

Contesta de forma clara y precisa. Si el fragmento no tiene suficiente información, indica claramente que se necesita más contexto.

Pregunta: {question}

Fragmento de reglas:
\"\"\"
{chunk}
\"\"\"

Respuesta:"""
            )

            answer = call_llm_api(answer_prompt)

            entry = {
                "prompt": f"Pregunta: {question}\n\nContexto:\n{chunk}\n\nRespuesta:",
                "completion": f" {answer}"
            }

            dataset.append(entry)
            total_questions_generated += 1

            # Sleep opcional
            time.sleep(random.uniform(config.MIN_SLEEP, config.MAX_SLEEP))

    print(f"\n💾 Guardando dataset en {TRAINING_DATA_PATH} ...")
    save_dataset(dataset)

    print(f"✅ Dataset generado: {TRAINING_DATA_PATH} ({total_questions_generated} ejemplos)")

# --------------------------------------------------------------

if __name__ == "__main__":
    main()
