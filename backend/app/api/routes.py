from fastapi import APIRouter, Query
from app.services.semantic_search import search_context
from app.services.generative_answer import generate_answer_openrouter
from app.services.history import get_history, save_history

router = APIRouter()


@router.get("/ask_rule")
def ask_rule(question: str = Query(..., min_length=5)):
    """
    API endpoint to answer MTG rule questions using semantic search and generation.

    Args:
        question (str): User's question.

    Returns:
        dict: Contains the question, the source context, and the AI-generated answer.
    """
    context = search_context(question)
    answer = generate_answer_openrouter(question, context)

    # Guardar en historial
    print(f"📚 Guardando pregunta en historial: '{question}'")
    save_history(question, context, answer)
    print("✅ Pregunta guardada en historial.")

    return {
        "question": question,
        "context_used": context,
        "answer": answer
    }


@router.get("/get_history")
def get_history_endpoint(limit: int = 10):
    """
    API endpoint to retrieve recent question history.

    Args:
        limit (int): Number of records to retrieve (default: 10).

    Returns:
        dict: List of questions and answers with timestamps.
    """
    MAX_LIMIT = 100
    safe_limit = min(limit, MAX_LIMIT)

    rows = get_history(safe_limit)

    return {
        "history": [
            {
                "timestamp": row[0],
                "question": row[1],
                "answer": row[2]
            }
            for row in rows
        ]
    }
