from fastapi import APIRouter, Query
from app.services.semantic_search import search_context
from app.services.generative_answer import generate_answer_openrouter

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


    return {
        "question": question,
        "context_used": context,
        "answer": answer
    }
