import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

def build_faiss_index(chunks: list[str], model_id: str = "all-MiniLM-L6-v2", output_dir: str = "./data/embeddings") -> None:
    """
    Builds a FAISS index from a list of text chunks and saves it along with the chunk data.

    Args:
        chunks (list): List of strings representing rule chunks.
        model_id (str): Name of the sentence transformer model.
        output_dir (str): Directory to store the FAISS index and chunks.
    """
    model = SentenceTransformer(model_id)
    embeddings = model.encode(chunks, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{output_dir}/faiss.index")
    with open(f"{output_dir}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
