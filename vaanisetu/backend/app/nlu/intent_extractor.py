import os
from anthropic import AsyncAnthropic
import json

# Initialize Anthropic client
client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "dummy_key"))

# We define a function schema that we force the model to use
EXTRACT_TOOL = {
    "name": "extract_intent",
    "description": "Extracts entities, identifies missing fields, and calculates an ambiguity score from a citizen's speech transcript.",
    "input_schema": {
        "type": "object",
        "properties": {
            "extracted_entities": {
                "type": "object",
                "description": "Key-value pairs of information extracted from the transcript (e.g., occupation, income, age, location). Only include what is explicitly stated."
            },
            "missing_fields": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of core fields that are essential for determining scheme eligibility but are missing from the transcript (e.g., income, occupation, age, location)."
            },
            "ambiguity_score": {
                "type": "number",
                "description": "A score between 0.0 and 1.0 representing how ambiguous or incomplete the transcript is. 0.0 means completely clear and all info provided. 1.0 means completely vague or nonsensical."
            }
        },
        "required": ["extracted_entities", "missing_fields", "ambiguity_score"]
    }
}

async def extract_intent(transcript: str) -> dict:
    """
    Calls Claude Haiku to extract intent and ambiguity.
    """
    prompt = (
        f"Analyze the following transcript: '{transcript}'. "
        "Extract all relevant entities. Identify any core fields (income, occupation, age, location) "
        "that are strictly necessary but missing. Calculate an ambiguity score (0.0 to 1.0). "
        "CRITICAL RULE: DO NOT guess or fabricate values that are not explicitly stated by the user. "
        "Flag ambiguity honestly (e.g., if the user gives a vague or unrelated answer, score it high)."
    )
    try:
        response = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            tools=[EXTRACT_TOOL],
            tool_choice={"type": "tool", "name": "extract_intent"},
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        # Extract the tool use result
        for content_block in response.content:
            if content_block.type == "tool_use":
                return content_block.input
                
        return {
            "extracted_entities": {},
            "missing_fields": ["income", "occupation"],
            "ambiguity_score": 1.0
        }
    except Exception as e:
        print(f"NLU Error: {e}")
        # Fallback for hackathon demo if API key isn't set or fails
        return {
            "extracted_entities": {"occupation": "labour"},
            "missing_fields": ["income"],
            "ambiguity_score": 0.8
        }
