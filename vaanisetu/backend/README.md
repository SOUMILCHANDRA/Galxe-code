# VaaniSetu Backend

Voice-first conversational decision-intelligence system for government scheme discovery.

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis:**
   The backend uses Redis for session management. You can run it via Docker:
   ```bash
   docker run -p 6379:6379 -d redis
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in the required keys:
   ```env
   OPENAI_API_KEY=sk-your-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
   REDIS_URL=redis://localhost:6379
   RF_MODEL_PATH=app/models/rf_eligibility_model.pkl
   ```

## Model Placement & Feature Schema

- **Location:** Drop your trained Random Forest model artifact at `backend/app/models/rf_eligibility_model.pkl`.
- **Feature Schema:** You must manually update `app/reasoning/feature_builder.py` to construct the exact feature vector (column order/encodings) that your Random Forest model expects based on the extracted entities and scheme features. Currently, it throws a `NotImplementedError` to prevent misaligned inference.

## Run the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Contract

The API is accessible under `http://localhost:8000/api`.

### 1. GET /health
Returns the operational status of core backend services.
**Output:**
```json
{
  "status": "ok",
  "redis_ok": true,
  "rf_model_loaded": true,
  "embedding_index_loaded": true
}
```

### 2. POST /asr
Converts audio speech to text using Whisper.
**Input:** `multipart/form-data`
- `audio`: The audio file blob
- `lang_hint` (optional): Hint for the detected language

**Output:**
```json
{
  "transcript": "...",
  "detected_lang": "hi"
}
```

### 3. POST /tts
Converts a text response into speech audio using Coqui TTS / gTTS.
**Input:** `application/json`
```json
{
  "text": "The response text here...",
  "lang": "en"
}
```
**Output:**
```json
{
  "audio_url": "http://localhost:8000/static/filename.wav"
}
```

### 4. POST /converse
Orchestrates the Intent -> Dialogue Manager -> Reasoning pipeline.
**Input:** `application/json`
```json
{
  "session_id": "unique-session-id",
  "transcript": "I am looking for a scheme..."
}
```
**Output (Clarify Mode):**
```json
{
  "mode": "clarify",
  "clarifying_question": {
    "text": "What is your annual income?",
    "options": null
  },
  "result": null
}
```
**Output (Result Mode):**
```json
{
  "mode": "result",
  "clarifying_question": null,
  "result": {
    "scheme": "PM Kisan",
    "confidence": 0.85,
    "missing_info": ["You are missing your Aadhaar card."],
    "reasoning_trace": ["Passed income check", "RF probability: 0.85"]
  }
}
```
