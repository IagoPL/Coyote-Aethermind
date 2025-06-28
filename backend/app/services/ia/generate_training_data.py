"""
generate_training_data.py

Generates a training dataset for the Aethermind AI model.

- Reads question/answer history stored in SQLite.
- Reads Magic rules chunks (FAISS embeddings).
- Builds training examples in the format:
    Question + Context → Answer
- Saves the dataset in .jsonl format (compatible with Huggingface).

Usage:
    python -m app.services.ia.generate_training_data

Output:
    data/training_data/training_data.jsonl
"""

import sqlite3
import json
import pickle
import os
from app.config import HISTORY_DB_PATH, CHUNKS_PATH, TRAINING_DATA_PATH

def load_chunks():
    """
    Loads Magic rules chunks from pickle file.

    Returns:
        list[str]: List of text chunks.
    """
    print(f"USANDO CHUNKS_PATH: {CHUNKS_PATH}")  # Para depuración
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return chunks

def load_history():
    """
    Loads question, context, and answer history from SQLite.

    Returns:
        list[tuple]: List of (question, context_used_json, answer) tuples.
    """
    print(f"USANDO HISTORY_DB_PATH: {HISTORY_DB_PATH}")  # Para depuración
    conn = sqlite3.connect(HISTORY_DB_PATH)
    conn.execute('PRAGMA journal_mode=DELETE;')  # 🔥 Forzar modo consistente
    cursor = conn.cursor()

    cursor.execute('''
        SELECT question, context_used, answer FROM history
    ''')

    rows = cursor.fetchall()
    conn.close()
    print(f"🔎 Se encontraron {len(rows)} registros en la tabla history.")
    return rows

def build_dataset(rows):
    """
    Builds the training dataset from history data.

    Args:
        rows (list[tuple]): List of (question, context_used_json, answer) tuples.

    Returns:
        list[dict]: List of examples in {'prompt': ..., 'completion': ...} format.
    """
    dataset = []

    for row in rows:
        question = row[0]
        context_json = row[1]
        answer = row[2]

        try:
            # Parsear el contexto que es un string JSON → lista
            context_list = json.loads(context_json)
            if not isinstance(context_list, list):
                context_list = []
        except Exception as e:
            print(f"⚠️ Error al parsear context_used para pregunta '{question}': {e}")
            context_list = []

        # Construir el ejemplo (aunque el contexto esté vacío)
        entry = {
            "prompt": f"Pregunta: {question}\n\nContexto:\n" + "\n".join(context_list) + "\n\nRespuesta:",
            "completion": f" {answer}"  # Espacio inicial recomendado
        }

        dataset.append(entry)

    return dataset

def save_dataset(dataset, output_path):
    """
    Saves the dataset in .jsonl format.

    Args:
        dataset (list[dict]): List of examples.
        output_path (str): Path to the .jsonl output file.
    """
    # Asegurarse que el directorio existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for entry in dataset:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

def main():
    """
    Main process of the script:
    - Loads chunks
    - Loads history
    - Builds dataset
    - Saves .jsonl
    """
    print("📚 Cargando chunks de reglas...")
    chunks = load_chunks()

    print("🗄️  Cargando historial de preguntas...")
    rows = load_history()

    print("🛠️  Construyendo dataset de entrenamiento...")
    dataset = build_dataset(rows)

    print("💾 Guardando dataset en .jsonl...")
    save_dataset(dataset, TRAINING_DATA_PATH)

    print(f"✅ Dataset generado: {TRAINING_DATA_PATH} ({len(dataset)} ejemplos)")

if __name__ == "__main__":
    main()
