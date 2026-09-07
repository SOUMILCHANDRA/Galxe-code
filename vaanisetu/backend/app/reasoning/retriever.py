import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Multilingual embedding model for code-mixed / Hindi speech
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Lazy-load to avoid startup blocking, or initialize here
_model = None
_collection = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.Client()
        _collection = client.create_collection(name="schemes")
        
        # Load and index
        schemes = load_schemes()
        if schemes:
            docs = []
            ids = []
            metadatas = []
            for s in schemes:
                docs.append(s.get("short_description", "") + " " + s.get("benefit_summary", ""))
                ids.append(s["id"])
                metadatas.append({"name": s["name"]})
            
            embeddings = get_model().encode(docs).tolist()
            _collection.add(
                embeddings=embeddings,
                documents=docs,
                metadatas=metadatas,
                ids=ids
            )
    return _collection

def load_schemes():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "schemes.json")
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r") as f:
        return json.load(f)

def retrieve_schemes(transcript: str, top_k: int = 3):
    """
    RAG shortlist over schemes using a multilingual sentence transformer.
    """
    collection = get_collection()
    if collection.count() == 0:
        return load_schemes()[:top_k] # fallback if empty
        
    query_embedding = get_model().encode([transcript]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # Map back to full scheme dicts
    all_schemes = {s["id"]: s for s in load_schemes()}
    retrieved = []
    if results["ids"] and results["ids"][0]:
        for scheme_id in results["ids"][0]:
            if scheme_id in all_schemes:
                retrieved.append(all_schemes[scheme_id])
                
    return retrieved
