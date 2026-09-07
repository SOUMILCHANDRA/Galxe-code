import os
import uuid
import asyncio
from gtts import gTTS

try:
    from TTS.api import TTS
    COQUI_AVAILABLE = True
    # Initialize the model once. For a fast demo, choose an efficient model.
    coqui_tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False).to("cpu")
except ImportError:
    COQUI_AVAILABLE = False
    coqui_tts = None
    print("Coqui TTS not installed. Falling back to gTTS exclusively.")

# Use the static directory mounted in main.py
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__dirname__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

async def synthesize(text: str, lang: str = "en", base_url: str = "http://localhost:8000") -> str:
    """
    Synthesizes speech using Coqui TTS (primary) or gTTS (fallback).
    Returns the URL to access the audio.
    """
    filename = f"{uuid.uuid4()}.wav" if COQUI_AVAILABLE else f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(STATIC_DIR, filename)

    try:
        def _generate():
            if COQUI_AVAILABLE:
                # Coqui implementation
                coqui_tts.tts_to_file(text=text, file_path=filepath)
            else:
                # gTTS Fallback
                tts = gTTS(text=text, lang=lang)
                tts.save(filepath)
                
        # Run blocking TTS generation in a thread
        await asyncio.to_thread(_generate)
        
        return f"{base_url}/static/{filename}"
    except Exception as e:
        print(f"TTS Error: {e}")
        # Secondary fallback if Coqui crashes during inference
        try:
            def _generate_fallback():
                tts = gTTS(text=text, lang=lang)
                tts.save(filepath.replace(".wav", ".mp3"))
            await asyncio.to_thread(_generate_fallback)
            return f"{base_url}/static/{filename.replace('.wav', '.mp3')}"
        except Exception as e2:
            print(f"gTTS Fallback Error: {e2}")
            return f"{base_url}/static/error.mp3"
