import os
import json
from typing import Dict, Any
import redis.asyncio as redis

# Default TTL for a conversation session (e.g., 30 minutes)
SESSION_TTL = 1800 

redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"), decode_responses=True)

async def get_session(session_id: str) -> Dict[str, Any]:
    """
    Retrieves the session state from Redis. If none exists, returns a default structure.
    """
    data = await redis_client.get(f"session:{session_id}")
    if data:
        return json.loads(data)
    
    return {
        "history": [],
        "extracted_entities": {},
        "asked_questions": []
    }

async def save_session(session_id: str, data: Dict[str, Any]):
    """
    Saves the session state to Redis with a TTL.
    """
    await redis_client.setex(
        f"session:{session_id}",
        SESSION_TTL,
        json.dumps(data)
    )
