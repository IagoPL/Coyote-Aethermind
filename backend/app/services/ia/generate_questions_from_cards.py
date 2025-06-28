import sqlite3
import json
import os
import random
from tqdm import tqdm
from app.config import TRAINING_DATA_DIR

# Ruta a la base de datos SQLite de MTGJSON
SQLITE_PATH = os.path.join(TRAINING_DATA_DIR, "mtgjson", "AllPrintings.sqlite")
OUTPUT_PATH = os.path.join(TRAINING_DATA_DIR, "card_generated", "card_qa_data.jsonl")

# Asegurarse de que el directorio existe
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def extract_cards_from_sqlite(limit=None):
    """
    Extrae cartas desde la base de datos SQLite de MTGJSON.
    """
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()

    query = """
    SELECT name, type, text, manaCost, power, toughness, loyalty
    FROM cards
    WHERE text IS NOT NULL
    """
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    cards = []
    for row in rows:
        name, type_, text, manaCost, power, toughness, loyalty = row
        cards.append({
            "name": name,
            "type": type_,
            "text": text,
            "manaCost": manaCost,
            "power": power,
            "toughness": toughness,
            "loyalty": loyalty
        })
    return cards

def generate_qa(card):
    """
    Genera una pregunta y respuesta sencilla a partir del texto de la carta.
    """
    question_templates = [
        "¿Qué hace la carta '{name}'?",
        "¿Cuál es la función de '{name}' en una partida?",
        "¿Cómo afecta '{name}' al juego?",
        "¿Qué habilidades tiene '{name}'?",
        "¿Qué representa la carta '{name}' en Magic?",
    ]
    question = random.choice(question_templates).format(name=card['name'])

    # La respuesta será simplemente el texto de reglas
    answer = card["text"]

    return {
        "prompt": f"Pregunta: {question}\n\nContexto:\nNombre: {card['name']}\nTipo: {card['type']}\n\nRespuesta:",
        "completion": f" {answer.strip()}"
    }

def main():
    print("📥 Extrayendo cartas desde MTGJSON SQLite...")
    cards = extract_cards_from_sqlite()
    print(f"📊 {len(cards)} cartas encontradas")

    print("🤖 Generando preguntas/respuestas...")
    dataset = []
    for card in tqdm(cards):
        qa = generate_qa(card)
        dataset.append(qa)

    print("💾 Guardando dataset...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in dataset:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

    print(f"✅ Dataset generado: {OUTPUT_PATH} ({len(dataset)} ejemplos)")

if __name__ == "__main__":
    main()
