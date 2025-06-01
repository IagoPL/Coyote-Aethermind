# Coyote-Aethermind

**Aethermind** es un asistente inteligente multiplataforma para jugadores de *Magic: The Gathering*, con IA para construir mazos, consultar reglas, trackear partidas y sugerir jugadas, usando tecnologías locales (ONNX, DirectML) y accesibles (API REST, PWA).

---

## 🚀 Características

- 🧠 Asistente de reglas de MTG (IA NLP + búsqueda semántica)
- 🃏 Recomendador de cartas y mazos (deckbuilder inteligente)
- ♟️ Seguimiento de estado de partida (zonas, fases, pila)
- 🤖 Sugerencias de jugadas y motor de validación
- 🌐 Interfaz accesible desde móvil, escritorio o navegador
- ⚡️ Aceleración en GPU AMD mediante ONNX + DirectML

---

## 📦 Estructura

- `backend/`: API en FastAPI + motor lógico + integración de IA
- `frontend/`: Interfaz en React/Tailwind (opcional Tauri para escritorio)
- `models/`: Modelos locales (ONNX, llama.cpp, etc.)
- `data/`: Reglas procesadas, embeddings y bases semánticas
- `docs/`: Documentación técnica y decisiones de arquitectura

---

## 🛠️ Tecnologías

- Python, FastAPI
- React + Tailwind CSS
- ONNX Runtime (DirectML), llama.cpp, OpenAI API
- FAISS, sentence-transformers
- Tauri (opcional)
