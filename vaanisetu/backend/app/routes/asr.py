from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
from app.asr.whisper_client import transcribe

router = APIRouter()

@router.post("/asr")
async def process_asr(
    audio: UploadFile = File(...),
    lang_hint: Optional[str] = Form(None)
):
    if not audio.filename:
        raise HTTPException(status_code=400, detail="Audio file must have a filename")
        
    try:
        audio_bytes = await audio.read()
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty")
            
        result = await transcribe(audio_bytes, lang_hint)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")
