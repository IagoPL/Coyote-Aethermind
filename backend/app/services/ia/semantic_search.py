import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("../data/embeddings/faiss.index")

with open("../data/embeddings/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def search_context(question: str, top_k: int = 8) -> list[str]:
    """
    Searches for the most semantically similar rule chunks to the user's question.

    Args:
        question (str): The user's query.
        top_k (int): Number of relevant results to return.

    Returns:
        List[str]: Top relevant rule chunks.
    """
    question_emb = model.encode([question])
    D, I = index.search(question_emb, top_k)
    return [chunks[i] for i in I[0]]
