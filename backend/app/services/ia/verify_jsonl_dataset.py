import json
import os

# Construye la ruta absoluta al dataset
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CURRENT_DIR, "../../../..", "data/training_data/combined/combined_training_data_deduplicated.jsonl")

# Cargamos y validamos
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

valid_count = 0
invalid_count = 0

for i, line in enumerate(lines):
    try:
        item = json.loads(line)
        if isinstance(item, dict) and "prompt" in item and "completion" in item:
            valid_count += 1
        else:
            print(f"❌ Entrada inválida en línea {i + 1}: {item}")
            invalid_count += 1
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON mal formado en línea {i + 1}: {e}")
        invalid_count += 1

print(f"\n✅ Total válidos: {valid_count}")
print(f"🛑 Total inválidos: {invalid_count}")
