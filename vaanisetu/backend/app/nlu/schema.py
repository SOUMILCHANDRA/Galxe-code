# NLU Schemas
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class IntentResult(BaseModel):
    extracted_entities: Dict[str, Any]
    missing_fields: List[str]
    ambiguity_score: float
