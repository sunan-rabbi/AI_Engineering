from sentence_transformers import SentenceTransformer  # type: ignore

EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(payload):
    """Encodes a single string or a list of strings and returns Python list(s)."""
    return EMBEDDING_MODEL.encode(payload).tolist()