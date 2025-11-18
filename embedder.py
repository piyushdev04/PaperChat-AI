from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-base-en-v1.5')

def embed_texts(texts):
    """
    Embeds a list of texts using bge-base-en-v1.5.
    Args:
        texts (List[str]): List of text chunks.
    Returns:
        List[List[float]]: List of embeddings.
    """
    return model.encode(texts, show_progress_bar=True, convert_to_numpy=True).tolist() 