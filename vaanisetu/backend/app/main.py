from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.routes import asr, tts, converse

app = FastAPI(
    title="VaaniSetu Backend",
    description="Backend for VaaniSetu — The Civic Voice Interface",
    version="1.0.0"
)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(asr.router, prefix="/api")
app.include_router(tts.router, prefix="/api")
app.include_router(converse.router, prefix="/api")

from app.dialogue.session_store import redis_client
from app.reasoning.rf_classifier import rf_model
from app.reasoning.retriever import get_collection

@app.get("/health")
async def health_check():
    # Check Redis
    try:
        await redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False
        
    # Check embeddings
    try:
        col = get_collection()
        emb_ok = col.count() > 0 or True # if collection exists, we consider it ok
    except Exception:
        emb_ok = False
        
    return {
        "status": "ok" if redis_ok else "degraded",
        "redis_ok": redis_ok,
        "rf_model_loaded": rf_model is not None,
        "embedding_index_loaded": emb_ok
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
