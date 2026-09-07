import os
import tempfile
from faster_whisper import WhisperModel
import asyncio

# Initialize the model on first import to save time. Using tiny/base for speed in a hackathon.
MODEL_SIZE = "tiny"
# Adjust compute_type to int8 or float32 if fp16 is not supported on the target CPU/GPU
whisper_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

async def transcribe(audio_bytes: bytes, lang_hint: str = None) -> dict:
    """
    Transcribes audio using faster-whisper.
    No autocorrect/normalization on the transcript.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    try:
        # Run inference in a threadpool so it doesn't block the async event loop
        def _transcribe():
            # If lang_hint is provided, whisper will try to use it
            segments, info = whisper_model.transcribe(temp_path, language=lang_hint)
            transcript = "".join(segment.text for segment in segments)
            return {
                "transcript": transcript.strip(),
                "detected_lang": info.language
            }
            
        result = await asyncio.to_thread(_transcribe)
        return result
    except Exception as e:
        print(f"ASR Error: {e}")
        return {
            "transcript": "",
            "detected_lang": lang_hint or "en"
        }
    finally:
        os.unlink(temp_path)
