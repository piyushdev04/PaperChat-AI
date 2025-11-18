import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()


def store_embeddings(chunks, embeddings, collection_name):
    """
    Stores text chunks and their embeddings in a ChromaDB collection.
    Args:
        chunks (List[str]): List of text chunks.
        embeddings (List[List[float]]): List of embeddings.
        collection_name (str): Name of the collection.
    """
    collection = client.get_or_create_collection(collection_name, embedding_function=None)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)


def query_top_k(query_embedding, collection_name, k=5):
    """
    Queries the collection for top-k most similar chunks to the query embedding.
    Args:
        query_embedding (List[float]): Embedding of the query.
        collection_name (str): Name of the collection.
        k (int): Number of top results to return.
    Returns:
        List[dict]: List of top-k results with 'id', 'document', and 'distance'.
    """
    collection = client.get_collection(collection_name)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    top_chunks = []
    for i in range(len(results['ids'][0])):
        top_chunks.append({
            'id': results['ids'][0][i],
            'document': results['documents'][0][i],
            'distance': results['distances'][0][i]
        })
    return top_chunks 