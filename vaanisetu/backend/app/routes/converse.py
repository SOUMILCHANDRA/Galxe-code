from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.nlu.intent_extractor import extract_intent
from app.dialogue.state_machine import process_turn
from app.reasoning.retriever import retrieve_schemes
from app.reasoning.hard_rule_gate import evaluate_hard_constraints
from app.reasoning.rf_classifier import score
from app.reasoning.synthesizer import generate_explanation

router = APIRouter()

class ConverseRequest(BaseModel):
    session_id: str
    transcript: str

class ClarifyingQuestion(BaseModel):
    text: str
    options: Optional[List[str]] = None

class ResultDetail(BaseModel):
    scheme: str
    confidence: float
    missing_info: List[str]
    reasoning_trace: List[str]

class ConverseResponse(BaseModel):
    mode: str # "clarify" | "result"
    clarifying_question: Optional[ClarifyingQuestion] = None
    result: Optional[ResultDetail] = None

@router.post("/converse", response_model=ConverseResponse)
async def converse(request: ConverseRequest):
    if not request.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="transcript cannot be empty")
        
    try:
        # 1. Intent & Ambiguity Extraction
        intent_result = await extract_intent(request.transcript)
        
        # 2. Dialogue Manager (Proceed or Clarify)
        turn_decision = await process_turn(request.session_id, request.transcript, intent_result)
        
        if turn_decision["mode"] == "clarify":
            return ConverseResponse(
                mode="clarify",
                clarifying_question=ClarifyingQuestion(
                    text=turn_decision["clarifying_question"]["text"]
                )
            )
            
        # 3. Reasoning Engine
        entities = turn_decision["entities"]
        
        # 3a. Retrieve potential schemes (RAG Shortlist)
        shortlisted_schemes = retrieve_schemes(request.transcript)
        
        # 3b. Rule Engine (Hard Constraints Gate)
        eligible_schemes = evaluate_hard_constraints(entities, shortlisted_schemes)
        
        # 3c. RF Model Scoring and Synthesis
        if not eligible_schemes:
            # Failed hard gate for all
            top_scheme = shortlisted_schemes[0] if shortlisted_schemes else {"name": "Unknown", "scheme_id": "UNKNOWN"}
            # For simplicity, assume they missed everything if it failed
            hard_gate_missing = ["Did not meet mandatory constraints"]
            rf_result = {"eligible_probability": 0.0}
        else:
            top_scheme = eligible_schemes[0]
            hard_gate_missing = []
            try:
                rf_result = score(entities, top_scheme)
            except NotImplementedError as e:
                rf_result = {"eligible_probability": 0.0, "error": str(e)}
                
        # 4. Explainable Response Synthesis
        final_result = await generate_explanation(entities, top_scheme.get("name", "Unknown Scheme"), rf_result, hard_gate_missing)
        
        return ConverseResponse(
            mode="result",
            result=ResultDetail(
                scheme=final_result["scheme"],
                confidence=final_result["confidence"],
                missing_info=final_result["missing_info"],
                reasoning_trace=final_result["reasoning_trace"]
            )
        )
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
