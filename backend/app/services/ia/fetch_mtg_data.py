import os
import requests
import hashlib
import json
from datetime import datetime

# === CONFIGURACION ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "training_data")
MTGJSON_DIR = os.path.join(DATA_DIR, "mtgjson")
SCRYFALL_DIR = os.path.join(DATA_DIR, "scryfall")

os.makedirs(MTGJSON_DIR, exist_ok=True)
os.makedirs(SCRYFALL_DIR, exist_ok=True)


def sha256sum_from_bytes(data):
    return hashlib.sha256(data).hexdigest()

def save_if_changed(path, data):
    new_hash = sha256sum_from_bytes(data)
    meta_path = path + ".meta"
    old_hash = None

    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            old_hash = f.read().strip()

    if new_hash != old_hash:
        with open(path, "wb") as f:
            f.write(data)
        with open(meta_path, "w") as f:
            f.write(new_hash)
        print(f"✅ Archivo actualizado: {os.path.basename(path)}")
    else:
        print(f"⏭️  Sin cambios: {os.path.basename(path)}")


# === MTGJSON ===
MTGJSON_FILES = {
    "AllPrintings.sqlite": "https://mtgjson.com/api/v5/AllPrintings.sqlite",
    "AllPrices.json": "https://mtgjson.com/api/v5/AllPrices.json",
    "AllSets.json": "https://mtgjson.com/api/v5/AllSets.json"
}

def fetch_mtgjson():
    print("\n📥 Descargando datos desde MTGJSON...")
    for filename, url in MTGJSON_FILES.items():
        dest_path = os.path.join(MTGJSON_DIR, filename)
        try:
            r = requests.get(url)
            r.raise_for_status()
            save_if_changed(dest_path, r.content)
        except Exception as e:
            print(f"⚠️  Error al descargar {filename}: {e}")


# === SCRYFALL ===
SCRYFALL_BULK_ENDPOINT = "https://api.scryfall.com/bulk-data"


def fetch_scryfall():
    print("\n📥 Descargando datos desde Scryfall...")
    try:
        r = requests.get(SCRYFALL_BULK_ENDPOINT)
        r.raise_for_status()
        bulk_data = r.json()
        with open(os.path.join(SCRYFALL_DIR, "bulk-data.json"), "w") as f:
            json.dump(bulk_data, f, indent=2)

        for obj in bulk_data["data"]:
            name = obj["type"]
            download_url = obj["download_uri"]
            filename = f"{name}.json"
            dest_path = os.path.join(SCRYFALL_DIR, filename)

            r2 = requests.get(download_url)
            r2.raise_for_status()
            save_if_changed(dest_path, r2.content)

    except Exception as e:
        print(f"⚠️  Error al descargar desde Scryfall: {e}")


def main():
    print("📦 Iniciando actualización de datasets de Magic...")
    fetch_mtgjson()
    fetch_scryfall()
    print("\n🎉 Actualización completada.")


if __name__ == "__main__":
    main()
