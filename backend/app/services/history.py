import sqlite3
import json
import os
from datetime import datetime

# Crear carpeta data si no existe
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'), exist_ok=True)

# Ruta absoluta al archivo DB
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'history.db')


def init_db():
    """
    Initializes the SQLite database.

    Creates the `history` table if it does not exist.

    The table contains:
    - id: Primary Key (autoincrement)
    - timestamp: UTC timestamp of the entry
    - question: User's question
    - context_used: JSON-serialized list of context chunks used for the answer
    - answer: The generated answer

    This function is called automatically on module import.
    """
    conn = sqlite3.connect(DB_PATH)
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


def save_history(question: str, context_used: list[str], answer: str):
    """
    Saves a question and its answer to the history database.

    Args:
        question (str): The user's question.
        context_used (list[str]): List of context chunks used for generating the answer.
        answer (str): The generated answer.

    The function inserts a new record into the `history` table with a UTC timestamp.
    """
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, question, answer FROM history
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# Initialize the database when the module is imported
init_db()
