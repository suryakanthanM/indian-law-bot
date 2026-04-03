import os
import json
import math
import urllib.request
from app.core.config import settings

# A pure-python in-memory vector database to bypass Windows SQLite/ChromaDB segfaults
DB_FILE = os.path.join(settings.VECTOR_DB_PATH, "simple_db.json")
memory_db = []

def load_db():
    global memory_db
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                memory_db = json.load(f)
        except Exception:
            memory_db = []

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_db, f)

load_db()

def get_google_embedding(text: str) -> list[float]:
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={api_key}"
    
    safe_text = text if text and text.strip() else "empty document"
    payload = {
        "model": "models/gemini-embedding-001",
        "content": {"parts": [{"text": safe_text}]}
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data["embedding"]["values"]
    except Exception as e:
        print(f"Error fetching embedding: {e}")
        return [0.0] * 768

def get_google_embeddings_batch(texts: list[str]) -> list[list[float]]:
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key={api_key}"
    
    requests = []
    for text in texts:
        safe_text = text if text and text.strip() else "empty document"
        requests.append({
            "model": "models/gemini-embedding-001",
            "content": {"parts": [{"text": safe_text}]}
        })
        
    payload = {"requests": requests}
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return [ans.get("values", [0.0]*768) for ans in data.get("embeddings", [])]
    except Exception as e:
        print(f"Error fetching batch embeddings: {e}")
        return [[0.0] * 768] * len(texts)

def add_to_db(documents: list[str], metadatas: list[dict], ids: list[str]):
    """Adds text chunks & their embeddings to the pure Python JSON database in fast batches."""
    global memory_db
    
    batch_size = 50
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        batch_embs = get_google_embeddings_batch(batch_docs)
        
        for j, emb in enumerate(batch_embs):
            memory_db.append({
                "id": batch_ids[j],
                "document": batch_docs[j],
                "metadata": batch_metas[j],
                "embedding": emb
            })
            
    print(f"Added {len(documents)} chunks to pure Python VectorDB.")
    save_db()

def cosine_similarity(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    if mag1 == 0 or mag2 == 0:
         return 0
    return dot / (mag1 * mag2)

def search_db(query: str, n_results: int = 3):
    """Searches the JSON database using cosine similarity."""
    q_emb = get_google_embedding(query)
    
    scored = []
    for entry in memory_db:
        score = cosine_similarity(q_emb, entry["embedding"])
        scored.append((score, entry))
        
    scored.sort(key=lambda x: x[0], reverse=True)
    top_entries = [x[1] for x in scored[:n_results]]
    
    # Format to match the old ChromaDB response structure
    return {
        "documents": [[e["document"] for e in top_entries]],
        "metadatas": [[e["metadata"] for e in top_entries]],
    }