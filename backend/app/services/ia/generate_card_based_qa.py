import os
import json
import random
from hashlib import md5
from pathlib import Path
from tqdm import tqdm
from app.config import DATA_DIR

# === CONFIGURACIÓN ===
SCRYFALL_DIR = os.path.join(DATA_DIR, "training_data", "scryfall")
OUTPUT_DIR = os.path.join(DATA_DIR, "training_data", "card_generated")
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

CARDS_PATH = os.path.join(SCRYFALL_DIR, "oracle_cards.json")
RULINGS_PATH = os.path.join(SCRYFALL_DIR, "rulings.json")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "card_qa_data.jsonl")

NUM_QUESTIONS = 72000  

# === FUNCIONES ===

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_existing_questions(path):
    existing = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    key = md5(obj["prompt"].encode()).hexdigest()
                    existing.add(key)
                except Exception:
                    continue
    return existing

def generate_prompt(card):
    # Ejemplos de preguntas diversas
    name = card.get("name", "")
    oracle_text = card.get("oracle_text", "")
    type_line = card.get("type_line", "")
    keywords = card.get("keywords", [])

    if not oracle_text:
        return None

    questions = [
        f"¿Qué hace la carta {name}?",
        f"¿Cómo funciona la habilidad {keywords[0]}?" if keywords else None,
        f"¿Qué ocurre si lanzo {name} fuera de mi turno?",
        f"¿Es legal {name} en Commander?",
        f"¿Qué reglas especiales tiene la carta {name}?",
        f"¿Qué tipo de criatura es {name}?",
        f"¿Cómo interactúa {name} con habilidades como Hexproof?",
    ]

    question = random.choice([q for q in questions if q])
    context = f"Nombre: {name}\nTipo: {type_line}\nTexto: {oracle_text}"
    return question, context

def find_ruling_answer(card, rulings):
    uri = card.get("rulings_uri", "")
    matching = [r for r in rulings if r.get("uri", "") == uri]
    if matching:
        entry = matching[0].get("data", [])
        if entry:
            return random.choice(entry).get("comment", "")
    return ""

def generate_examples(cards, rulings, existing_hashes, limit):
    dataset = []
    random.shuffle(cards)

    for card in tqdm(cards[:2000]):
        result = generate_prompt(card)
        if not result:
            continue

        question, context = result
        key = md5(question.encode()).hexdigest()
        if key in existing_hashes:
            continue

        answer = find_ruling_answer(card, rulings) or "Respuesta no disponible basada en reglas oficiales."
        example = {
            "prompt": f"{question}\n\nContexto:\n{context}\n\nRespuesta:",
            "completion": f" {answer}"
        }

        dataset.append(example)
        existing_hashes.add(key)

        if len(dataset) >= limit:
            break

    return dataset

def save_dataset(dataset, output_path):
    with open(output_path, "a", encoding="utf-8") as f:
        for entry in dataset:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

# === MAIN ===

def main():
    print("📥 Cargando cartas y rulings de Scryfall...")
    cards = load_json(CARDS_PATH)
    rulings = load_json(RULINGS_PATH)

    print("📊 Cargando preguntas existentes...")
    existing_hashes = load_existing_questions(OUTPUT_PATH)

    print("🤖 Generando ejemplos únicos...")
    new_data = generate_examples(cards, rulings, existing_hashes, NUM_QUESTIONS)

    print(f"💾 Guardando {len(new_data)} nuevos ejemplos...")
    save_dataset(new_data, OUTPUT_PATH)

    print("✅ Finalizado.")

if __name__ == "__main__":
    main()
