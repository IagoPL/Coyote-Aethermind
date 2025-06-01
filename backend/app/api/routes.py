from fastapi import APIRouter, Query
from app.services.semantic_search import search_context

router = APIRouter()

@router.get("/ask_rule")
def ask_rule(question: str = Query(..., min_length=5)):
    """
    API endpoint to retrieve rules relevant to a user's question using semantic search.

    Args:
        question (str): The user's rules-related question.

    Returns:
        dict: Contains the original question and top matching rule sections.
    """
    context = search_context(question)
    return {
        "question": question,
        "context": context
    }
