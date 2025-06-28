import sqlite3
import json
import os

from datetime import datetime
from app.config import HISTORY_DB_PATH


def init_db():
    """
    Initializes the SQLite database.
    """
    print(f"USANDO HISTORY_DB_PATH: {HISTORY_DB_PATH}")  # Para depuración

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(HISTORY_DB_PATH), exist_ok=True)

    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            context_used TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Tabla 'history' creada o ya existente.")


def save_history(question: str, context_used: list[str], answer: str):
    """
    Saves a question and its answer to the history database.

    Args:
        question (str): The user's question.
        context_used (list[str]): List of context chunks used for generating the answer.
        answer (str): The generated answer.

    The function inserts a new record into the `history` table with a UTC timestamp.
    """
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()
    context_json = json.dumps(context_used, ensure_ascii=False, indent=2)

    cursor.execute('''
        INSERT INTO history (timestamp, question, context_used, answer)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, question, context_json, answer))

    conn.commit()
    conn.close()

def get_history(limit: int = 10):
    """
    Retrieves the latest entries from the history database.

    Args:
        limit (int): Number of records to retrieve. Defaults to 10.

    Returns:
        list[tuple]: List of tuples, each containing (timestamp, question, answer).
    """
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, question, answer FROM history
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows

def clear_history():
    """
    Clears all entries from the history table.
    """
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM history')

    conn.commit()
    conn.close()
    print("🗑️ Historial limpiado.")

def print_history(limit: int = 10):
    """
    Prints the latest entries from the history table.

    Args:
        limit (int): Number of records to print. Defaults to 10.
    """
    history = get_history(limit)
    print(f"\nÚltimas {len(history)} entradas del historial:")
    for entry in history:
        timestamp, question, answer = entry
        print(f"\n[{timestamp}]\nPregunta: {question}\nRespuesta: {answer}\n{'-'*40}")

# Initializa la base de datos 
if __name__ == "__main__":
    init_db()
    print_history(5)
