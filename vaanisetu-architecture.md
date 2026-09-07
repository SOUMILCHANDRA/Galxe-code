# VaaniSetu — System Architecture & Technical Specification

**Project:** VaaniSetu — The Civic Voice Interface
**Type:** Voice-first conversational decision-intelligence system for government scheme discovery
**Scope:** Round 1 hackathon MVP (5-hour build window), architected to extend to production

---

## 1. Design Principles

1. **Never fabricate an answer under ambiguity** — the dialogue manager gates every response behind an explicit ambiguity/confidence score. No confidence → no answer, only a clarifying question.
2. **Voice is the primary surface, not a bolt-on** — ASR/TTS sit at the edge of every turn, not behind a text-first chat UI.
3. **Reasoning is explainable** — every eligibility result ships with a confidence score and the specific missing proof/information, never a bare yes/no.
4. **Stateless where possible, session-scoped where not** — no PII persistence in Round 1; conversation state lives in Redis with a TTL, not a database.
5. **Swappable model layer** — LLM calls (intent extraction, synthesis) go through a thin adapter so GPT-4o-mini / Claude Haiku / Llama-3 are interchangeable without touching business logic.

---

## 2. High-Level Pipeline (6 Stages + Feedback Loop)

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────┐
│ 1. Citizen  │ ──▶ │ 2. ASR       │ ──▶ │ 3. Intent &        │
│    Speech   │     │ (Whisper)    │     │    Ambiguity       │
└─────────────┘     └──────────────┘     │    Extraction (LLM)│
                                          └─────────┬──────────┘
                                                    │
                                                    ▼
                                          ┌───────────────────┐
                            ┌────────────▶│ 4. Dialogue        │
                            │             │    Manager         │
                            │             │ (proceed/clarify)  │
                            │  clarify    └─────────┬──────────┘
                            │                       │ proceed
                            │                       ▼
                    ┌───────┴───────┐     ┌───────────────────┐
                    │ Clarifying     │◀────│ (ambiguity high)  │
                    │ question (TTS) │     └───────────────────┘
                    └────────────────┘               │
                                                    ▼
                                          ┌───────────────────┐
                                          │ 5. Reasoning Engine │
                                          │  RAG (FAISS/Chroma)│
                                          │  + Rule Engine      │
                                          └─────────┬──────────┘
                                                    │
                                                    ▼
                                          ┌───────────────────┐
                                          │ 6. Explainable     │
                                          │  Response + TTS    │
                                          │  (confidence +     │
                                          │   missing proof)   │
                                          └───────────────────┘
```

The **feedback loop** at stage 4 is the core differentiator: any turn can route back to a clarifying question instead of falling through to stage 5.

---

## 3. Component Breakdown

### 3.1 Voice Capture (Frontend edge)
- Captures mic input in-browser (Web Speech API) or in-app (React Native mic module).
- Streams/pushes audio blob to backend `/asr` endpoint; no client-side transcription in Round 1 (keeps model behavior consistent across web/mobile).

### 3.2 ASR — Speech to Text
- **Whisper** (multilingual) run via API or local `whisper.cpp`/`faster-whisper` for cost control.
- Output: raw transcript + detected language code, passed downstream unmodified (no autocorrect — informal/mixed-dialect speech is a feature of the input, not noise to strip).

### 3.3 Intent & Ambiguity Extraction (LLM, function-calling)
- Single LLM call with a structured function-calling schema that returns:
  - `extracted_entities` (occupation, income band, location, family status, etc. — whatever the transcript actually contains)
  - `missing_fields` (what the schema expects but the transcript didn't supply)
  - `ambiguity_score` (0–1)
- Model-agnostic adapter: GPT-4o-mini / Claude Haiku / Llama-3 all implement the same `extract(transcript) -> IntentResult` interface.

### 3.4 Dialogue Manager
- Python state machine (per-session) backed by Redis.
- Decision rule: `ambiguity_score > threshold` → emit ONE targeted clarifying question (not a form); else → proceed to reasoning engine.
- Tracks turn history and previously-asked clarifications so the same question is never re-asked.

### 3.5 Reasoning Engine
- **Retrieval (RAG):** sentence-transformer embeddings over the scheme dataset, indexed in FAISS (or Chroma for simpler local dev) → top-k relevant scheme documents.
- **Eligibility rule engine:** deterministic JSON-rule evaluation (income thresholds, occupation category, location, documentation) run against extracted entities.
- **Synthesis:** LLM combines retrieved scheme text + rule engine output + confidence into a structured explanation — the LLM narrates, the rule engine decides.

### 3.6 Explainable Response
- Structured output: matched scheme(s), eligibility confidence bar, exact missing proof/info, reasoning trace (which rules fired, which fields were assumed vs. confirmed).
- Multilingual TTS (Coqui TTS for offline/free, gTTS as a simpler fallback) renders the response back to speech.

---

## 4. Detailed Tech Stack

| Layer | Technology | Role | Notes / Alternatives |
|---|---|---|---|
| Voice capture | Web Speech API (web) / React Native mic module (mobile) | Capture raw audio | No client-side ASR — keep transcription server-side and uniform |
| Speech-to-text | OpenAI Whisper (multilingual) | Audio → transcript + language | `faster-whisper`/`whisper.cpp` for local/free inference if API cost is a constraint |
| Intent & ambiguity extraction | LLM function-calling — GPT-4o-mini / Claude Haiku / Llama-3 | Transcript → entities + missing fields + ambiguity score | Adapter pattern so the model is swappable without touching downstream logic |
| Dialogue management | Python state machine + Redis session store | Turn tracking, proceed-vs-clarify decision, session TTL | Redis chosen over a DB — no PII persistence needed for Round 1 |
| Knowledge base | Structured scheme dataset — JSON (rules, documents, steps) | Source of truth for schemes | 6–8 synthetic schemes for Round 1; myScheme.gov.in / data.gov.in for production |
| Retrieval | Sentence-transformer embeddings + FAISS or Chroma (RAG) | Semantic search over scheme text | Chroma is faster to stand up for a hackathon; FAISS if you need raw speed at scale |
| Eligibility reasoning | Hybrid: deterministic rule engine + LLM synthesis, confidence-scored | Decide eligibility, explain it | Rule engine owns the decision; LLM owns the explanation — keeps answers auditable |
| Text-to-speech | Coqui TTS (multilingual, self-hosted) / gTTS (simple, free) | Response → speech | Coqui for quality/offline; gTTS as the fast fallback if setup time is tight |
| Backend | Python · FastAPI | Orchestration, all six stages | Async endpoints for ASR/TTS I/O-bound calls |
| Frontend | React (web) / Flutter (mobile) | Three core screens (listening / clarifying / result) | Shared design language; mobile is the priority surface for the target users |
| Session/state store | Redis | Ephemeral per-session context | TTL-expired, no persistence — matches the privacy stance |

**Hard constraint carried over from the problem statement:** Round 1 has no requirement for full government integration, perfect ASR, complete policy coverage, or production deployment — the stack above is scoped for reasoning-quality and adaptability demos, not production hardening.

---

## 5. Repository Structure

```
vaanisetu/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entrypoint
│   │   ├── routes/
│   │   │   ├── asr.py              # POST /asr
│   │   │   ├── converse.py         # POST /converse (intent → dialogue → reasoning)
│   │   │   └── tts.py              # POST /tts
│   │   ├── asr/
│   │   │   └── whisper_client.py
│   │   ├── nlu/
│   │   │   ├── intent_extractor.py # LLM function-calling adapter
│   │   │   └── schema.py           # IntentResult, ambiguity scoring
│   │   ├── dialogue/
│   │   │   ├── state_machine.py
│   │   │   └── session_store.py    # Redis wrapper
│   │   ├── reasoning/
│   │   │   ├── retriever.py        # FAISS/Chroma RAG
│   │   │   ├── rule_engine.py      # JSON rule evaluation
│   │   │   └── synthesizer.py      # LLM explanation generation
│   │   ├── tts/
│   │   │   └── tts_client.py
│   │   └── data/
│   │       └── schemes.json        # 6–8 synthetic schemes
│   ├── requirements.txt
│   └── tests/
├── frontend-web/                   # React
│   └── src/screens/{Listening,Clarifying,Result}.tsx
├── frontend-mobile/                 # Flutter
│   └── lib/screens/
├── docs/
│   └── vaanisetu-architecture.md   # this file
└── README.md
```

---

## 6. Core API Contracts

```
POST /asr
  in:  { audio: blob, lang_hint?: string }
  out: { transcript: string, detected_lang: string }

POST /converse
  in:  { session_id: string, transcript: string }
  out: { mode: "clarify" | "result",
         clarifying_question?: { text: string, options?: string[] },
         result?: { scheme: string, confidence: number,
                    missing_info: string[], reasoning_trace: string[] } }

POST /tts
  in:  { text: string, lang: string }
  out: { audio_url: string }
```

`/converse` is the orchestration boundary — everything from intent extraction through reasoning happens behind it, one call per turn.

---

## 7. Build Plan → Engineering Tasks (5-hour window)

| Phase | Focus | Concrete deliverables |
|---|---|---|
| Hour 1 | Foundations | `schemes.json` (6–8 synthetic schemes), FastAPI skeleton with stub routes, React/Flutter shell with 3 empty screens |
| Hour 2 | Voice loop | Whisper wired into `/asr`, TTS wired into `/tts`, end-to-end round-trip returning a hardcoded stub reply |
| Hour 3 | Reasoning brain | `intent_extractor.py` (LLM function-calling), `state_machine.py` clarify-vs-proceed logic |
| Hour 4 | Eligibility engine | `retriever.py` (RAG over schemes) + `rule_engine.py` + confidence-scored `synthesizer.py` |
| Hour 5 | Integrate & demo | Full pipeline wired end-to-end, reasoning trace visible in UI, rehearse the ambiguous-query demo |

**Demo script:** open with an incomplete/informal query ("I don't have a fixed job, sometimes I do labour work") → system asks one sharp clarifying question → reasons to a scheme match with a stated confidence level.

---

## 8. Explicit Non-Goals (Round 1)

- Full integration with government systems (myScheme, data.gov.in APIs) — synthetic dataset only.
- Production-grade ASR accuracy across all Indian languages.
- Complete policy/scheme coverage.
- Persistent user accounts or PII storage.
- Production deployment/scaling — local or single-instance demo only.
