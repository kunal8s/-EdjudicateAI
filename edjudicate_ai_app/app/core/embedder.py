from sentence_transformers import SentenceTransformer

_embedder = None


def _get_model():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedder


def embed_texts(texts):
    model = _get_model()
    return model.encode(texts, convert_to_tensor=False).tolist()