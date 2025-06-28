import os
import json
import hashlib
from pathlib import Path
from app.config import TRAINING_DATA_PATH, DATA_DIR

# Paths
CARD_DATA_PATH = os.path.join(DATA_DIR, "training_data", "card_generated", "card_qa_data.jsonl")
FULL_CARD_DATA_PATH = os.path.join(DATA_DIR, "training_data", "card_generated", "card_qa_data.jsonl")
COMBINED_DIR = os.path.join(DATA_DIR, "training_data", "combined")
COMBINED_PATH = os.path.join(COMBINED_DIR, "combined_training_data.jsonl")

Path(COMBINED_DIR).mkdir(parents=True, exist_ok=True)

def load_jsonl(path):
    if not os.path.exists(path):
        print(f"⚠️ Archivo no encontrado: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def save_jsonl(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

def deduplicate_entries(entries):
    seen = set()
    deduped = []

    for entry in entries:
        prompt = entry.get("prompt", "")
        key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        if key not in seen:
            seen.add(key)
            deduped.append(entry)

    return deduped

def main():
    print("📥 Cargando dataset desde historial...")
    history_data = load_jsonl(TRAINING_DATA_PATH)
    print(f"📊 {len(history_data)} ejemplos desde historial")

    print("📥 Cargando dataset generado de cartas...")
    card_data = load_jsonl(CARD_DATA_PATH)
    print(f"📊 {len(card_data)} ejemplos desde generación previa")

    print("📥 Cargando dataset extendido de cartas...")
    full_card_data = load_jsonl(FULL_CARD_DATA_PATH)
    print(f"📊 {len(full_card_data)} ejemplos desde dataset completo")

    combined = history_data + card_data + full_card_data
    print(f"🔗 Combinando datasets: {len(combined)} ejemplos totales (antes de filtrar)")

    combined_deduped = deduplicate_entries(combined)
    print(f"✅ Eliminados duplicados: {len(combined_deduped)} ejemplos finales")

    print("💾 Guardando archivo combinado...")
    save_jsonl(combined_deduped, COMBINED_PATH)
    print(f"📁 Guardado en: {COMBINED_PATH}")

if __name__ == "__main__":
    main()
