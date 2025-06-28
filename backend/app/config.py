"""
config.py

Global configuration for Aethermind backend.

This module defines consistent paths for:
- data directory (root /data)
- embeddings directory
- app runtime data (backend/app/data)
- history database (runtime)
- training data output (training datasets for model)

✅ Paths are always relative to the project root (one level above 'backend').
✅ Works correctly when running:
    - python build_index.py
    - python -m app.services...
    - uvicorn app.main:app
    - training scripts

"""

import os

# Detect project root (two levels above this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# General data directory (for embeddings, training data, etc.)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
EMBEDDINGS_DIR = os.path.join(DATA_DIR, 'embeddings')
CHUNKS_PATH = os.path.join(EMBEDDINGS_DIR, 'chunks.pkl')
FAISS_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, 'faiss.index')

# App runtime data (for history.db, logs, etc.)
APP_DATA_DIR = os.path.join(PROJECT_ROOT, 'backend', 'app', 'data')
APP_HISTORY_DIR = os.path.join(APP_DATA_DIR, 'history')
HISTORY_DB_PATH = os.path.join(APP_HISTORY_DIR, 'history.db')

# Training data
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training_data")
TRAINING_DATA_PATH = os.path.join(TRAINING_DATA_DIR, "training_data.jsonl")

# Optional: Print paths for debug (you can comment these out later)
if __name__ == "__main__":
    print("=== Project Paths ===")
    print(f"PROJECT_ROOT      : {PROJECT_ROOT}")
    print(f"DATA_DIR          : {DATA_DIR}")
    print(f"EMBEDDINGS_DIR    : {EMBEDDINGS_DIR}")
    print(f"CHUNKS_PATH       : {CHUNKS_PATH}")
    print(f"FAISS_INDEX_PATH  : {FAISS_INDEX_PATH}")
    print(f"TRAINING_DATA_DIR : {TRAINING_DATA_DIR}")
    print(f"TRAINING_DATA_PATH: {TRAINING_DATA_PATH}")
    print(f"APP_DATA_DIR      : {APP_DATA_DIR}")
    print(f"APP_HISTORY_DIR   : {APP_HISTORY_DIR}")
    print(f"HISTORY_DB_PATH   : {HISTORY_DB_PATH}")
