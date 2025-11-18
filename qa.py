import requests
from embedder import embed_texts
from db import query_top_k

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def answer_question(question, collection_name):
    question_embedding = embed_texts([question])[0]
    top_chunks = query_top_k(question_embedding, collection_name, k=2)
    context = '\n\n'.join([chunk['document'] for chunk in top_chunks])
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    result = response.json()
    return result.get("response", "").strip() 