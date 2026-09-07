from app.dialogue.session_store import get_session, save_session
from typing import Dict, Any

AMBIGUITY_THRESHOLD = 0.4

def select_clarifying_question(missing_fields: list, asked_questions: list) -> str:
    # A mapping prioritized by highest disambiguation value
    questions = {
        "income": "Could you please tell me your approximate annual family income?",
        "occupation": "What kind of work do you do to earn a living?",
        "age": "How old are you?",
        "location_type": "Do you live in an urban city or a rural village?",
        "documents": "What official identification documents do you currently have?"
    }
    
    for field in missing_fields:
        if field not in asked_questions and field in questions:
            return field, questions[field]
            
    # Fallback if we have unmapped fields or everything was asked
    for field in missing_fields:
        if field not in asked_questions:
            return field, f"Could you provide more information regarding your {field}?"
            
    return None, None

async def process_turn(session_id: str, transcript: str, intent_result: dict) -> Dict[str, Any]:
    session = await get_session(session_id)
    
    # Accumulate entities across turns
    session["extracted_entities"].update(intent_result.get("extracted_entities", {}))
    session["history"].append({"role": "user", "content": transcript})
    
    ambiguity = intent_result.get("ambiguity_score", 1.0)
    
    # Filter missing_fields to only those that we haven't successfully extracted yet
    missing = [f for f in intent_result.get("missing_fields", []) if f not in session["extracted_entities"]]
    
    if ambiguity > AMBIGUITY_THRESHOLD and missing:
        field, question = select_clarifying_question(missing, session["asked_questions"])
        
        if field:
            session["asked_questions"].append(field)
            session["history"].append({"role": "system", "content": question})
            await save_session(session_id, session)
            
            return {
                "mode": "clarify",
                "clarifying_question": {
                    "text": question
                },
                "entities": session["extracted_entities"]
            }
    
    # Ready to proceed to reasoning
    await save_session(session_id, session)
    return {
        "mode": "result",
        "entities": session["extracted_entities"]
    }
