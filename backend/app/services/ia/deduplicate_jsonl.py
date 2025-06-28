import os
import json

# Ruta base relativa al archivo combinado
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../data/training_data/combined")
)
INPUT_PATH = os.path.join(BASE_DIR, "combined_training_data.jsonl")
OUTPUT_PATH = os.path.join(BASE_DIR, "combined_training_data_deduplicated.jsonl")

def deduplicate_jsonl(input_path, output_path):
    seen = set()
    total = 0
    unique = 0

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            total += 1
            try:
                entry = json.loads(line)
                prompt = entry.get("prompt", "").strip()

                # Si el prompt ya fue procesado, se omite
                if prompt not in seen:
                    seen.add(prompt)
                    json.dump(entry, outfile, ensure_ascii=False)
                    outfile.write('\n')
                    unique += 1
            except json.JSONDecodeError:
                continue  # Ignora líneas corruptas

    print(f"🔍 Procesados: {total}")
    print(f"✅ Ejemplos únicos guardados: {unique}")
    print(f"🧹 Duplicados o inválidos eliminados: {total - unique}")
    print(f"📁 Guardado en: {output_path}")

if __name__ == "__main__":
    deduplicate_jsonl(INPUT_PATH, OUTPUT_PATH)
