from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.tts.tts_client import synthesize

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/tts")
async def process_tts(request: TTSRequest, req: Request):
    base_url = str(req.base_url).rstrip("/")
    audio_url = await synthesize(request.text, request.lang, base_url)
    return {
        "audio_url": audio_url
    }
