def split_text_into_chunks(text, chunk_size=500):
    """
    Splits text into chunks of approximately chunk_size tokens (words).
    Args:
        text (str): The input text.
        chunk_size (int): Number of tokens per chunk.
    Returns:
        List[str]: List of text chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks 