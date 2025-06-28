# bulk_ask.py

"""
Bulk Ask Script

This script sends a large number of diverse Magic: The Gathering questions
to the running Aethermind backend (/ask_rule endpoint).

Questions and answers will be saved automatically in history.db.

Usage:
    python bulk_ask.py
"""

import requests
import random
import time

# URL del backend
BASE_URL = "http://127.0.0.1:8000/ask_rule"

# Número de preguntas que quieres generar
NUM_QUESTIONS = 750

# Pool de plantillas
QUESTION_TEMPLATES = [
    "¿Qué es {}?",
    "¿Cómo funciona {}?",
    "¿Qué ocurre si uso {} con {}?",
    "¿Qué pasa si mi oponente juega {}?",
    "¿Puedo responder con {} a {}?",
    "¿Se puede prevenir {} con {}?",
    "¿Qué sucede si copio un hechizo con {}?",
    "¿En qué orden se resuelven {} y {}?",
    "¿Cómo afecta {} a {}?",
    "¿Qué interacción hay entre {} y {}?",
]

# Keywords / habilidades / conceptos de MTG
KEYWORDS = [
    "la pila",
    "storm",
    "protection",
    "trample",
    "first strike",
    "double strike",
    "lifelink",
    "deathtouch",
    "flashback",
    "morph",
    "cascade",
    "split second",
    "counterspell",
    "copy",
    "combat damage",
    "planeswalker",
    "legend rule",
    "state-based actions",
    "priority",
    "replacement effect",
    "triggered ability",
    "continuous effect",
    "mana ability",
    "static ability",
    "layers",
    "timestamp",
    "two-headed giant",
    "commander damage",
    "partner",
    "saga",
    "crew",
    "modular",
    "equip",
    "meld",
    "venture into the dungeon",
    "initiative",
    "poison counters",
    "emblem",
    "combat phase",
    "turn structure",
    "stack",
]

def generate_question():
    """
    Generates a random Magic rules question using 1 or 2 keywords as needed.
    """
    template = random.choice(QUESTION_TEMPLATES)
    k1 = random.choice(KEYWORDS)
    k2 = random.choice(KEYWORDS)

    num_placeholders = template.count("{}")

    if num_placeholders == 2:
        return template.format(k1, k2)
    elif num_placeholders == 1:
        return template.format(k1)
    else:
        return template  # por si alguna plantilla no tiene {}

def ask_question(question):
    """
    Sends a question to the backend and prints the answer.
    """
    try:
        response = requests.get(BASE_URL, params={"question": question})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pregunta: {question}")
            print(f"➡️  Respuesta: {data.get('answer', 'Sin respuesta')}")
            print("-" * 50)
        else:
            print(f"⚠️ Error ({response.status_code}) al preguntar: {question}")

    except Exception as e:
        print(f"⚠️ Excepción al preguntar: {question} | Error: {e}")

def main():
    print(f"🚀 Iniciando generación de {NUM_QUESTIONS} preguntas...")
    for i in range(NUM_QUESTIONS):
        question = generate_question()
        ask_question(question)
        time.sleep(random.uniform(0.5, 1.5))  # Evitar spam excesivo al backend
    print("✅ Finalizado.")

if __name__ == "__main__":
    main()
