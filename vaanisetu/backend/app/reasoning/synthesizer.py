import os
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "dummy_key"))

async def generate_explanation(entities: dict, scheme_name: str, rf_result: dict, hard_gate_missing: list) -> dict:
    """
    LLM call combining scheme text + hard-gate result + RF probability into a natural-language explanation.
    """
    prob = rf_result.get("eligible_probability", 0.0)
    
    if hard_gate_missing:
        # Failed hard constraints
        missing_str = ", ".join(hard_gate_missing)
        prompt = (
            f"The citizen applied for {scheme_name} but failed mandatory criteria. "
            f"Missing or invalid info: {missing_str}. "
            "Explain plainly to the citizen why they are ineligible based on these missing criteria. "
            "CRITICAL: Do not alter the verdict or fabricate information. Only explain plainly."
        )
        prob = 0.0
    else:
        # Passed hard constraints, scored by RF
        prompt = (
            f"The citizen applied for {scheme_name} and passed mandatory criteria. "
            f"Their Random Forest model eligibility probability is {prob*100}%. "
            f"Explain plainly to the citizen what this score means for their application. "
            "CRITICAL: Do not alter the verdict or probability. Only explain it plainly."
        )
    
    try:
        response = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = response.content[0].text
    except Exception as e:
        print(f"Synthesis error: {e}")
        explanation = "We encountered an error generating your explanation."

    return {
        "scheme": scheme_name,
        "confidence": prob,
        "missing_info": [explanation],
        "reasoning_trace": [
            f"Hard gate missing: {hard_gate_missing}",
            f"RF Probability: {prob}",
            f"RF Importances: {rf_result.get('feature_importances_for_this_call', {})}"
        ]
    }
