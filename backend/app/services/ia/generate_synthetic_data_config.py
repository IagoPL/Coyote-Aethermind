"""
generate_synthetic_data_config.py

Configuration for generate_synthetic_data.py
"""

# Number of questions to generate per chunk
NUM_QUESTIONS_PER_CHUNK = 3  # Puedes probar con 3 al principio, luego subir a 5 o más

# API endpoint to use (example with Puter API)
API_URL = "https://api.puter.com/ai/chat"

# Model name (optional, if your API supports it)
MODEL = "gpt-4o"

# Sleep between API calls (in seconds, to avoid rate limits)
MIN_SLEEP = 0.5
MAX_SLEEP = 1.0
