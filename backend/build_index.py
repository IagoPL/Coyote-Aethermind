import os
from backend.app.services.ia.preprocess_rules import split_rules_into_chunks
from backend.app.services.ia.embedding_index import build_faiss_index

def main():
    # Ruta del archivo de reglas
    rules_path = "../data/rules_raw/MagicCompRules.txt"
    output_dir = "../data/embeddings"

    # Verificar existencia
    if not os.path.exists(rules_path):
        print(f"❌ Rules file not found at {rules_path}")
        return

    # Dividir en chunks
    print("📖 Splitting rules into chunks...")
    chunks = split_rules_into_chunks(rules_path)

    # Construir índice
    print(f"🔍 Building FAISS index with {len(chunks)} chunks...")
    os.makedirs(output_dir, exist_ok=True)
    build_faiss_index(chunks, output_dir=output_dir)

    print("✅ Index built successfully!")

if __name__ == "__main__":
    main()
