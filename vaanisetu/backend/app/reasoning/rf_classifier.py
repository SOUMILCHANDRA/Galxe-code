import joblib
import os
import numpy as np
from app.reasoning.feature_builder import build_features

MODEL_PATH = os.environ.get("RF_MODEL_PATH", "app/models/rf_eligibility_model.pkl")

# Lazy-load RF model at startup
try:
    if os.path.exists(MODEL_PATH):
        rf_model = joblib.load(MODEL_PATH)
        print(f"Loaded RF model from {MODEL_PATH}")
    else:
        rf_model = None
        print(f"RF model not found at {MODEL_PATH}. Using mock confidence scoring.")
except Exception as e:
    print(f"Error loading RF model: {e}")
    rf_model = None

def score(entities: dict, scheme: dict) -> dict:
    """
    Scores eligibility using the pre-trained Random Forest model.
    Returns {eligible_probability: float, feature_importances_for_this_call: dict}
    """
    if rf_model is None:
        # Fallback if no model is provided
        return {
            "eligible_probability": 0.85,
            "feature_importances_for_this_call": {"mock_feature": 1.0}
        }
        
    try:
        feature_vector = build_features(entities, scheme)
        
        proba = rf_model.predict_proba(feature_vector)[0]
        # Assume class 1 is "eligible".
        prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        
        # Get global feature importances as rough explanation aid if available
        importances = {}
        if hasattr(rf_model, "feature_importances_"):
            global_importances = rf_model.feature_importances_
            for i, imp in enumerate(global_importances):
                importances[f"feature_{i}"] = float(imp)
                
        return {
            "eligible_probability": prob,
            "feature_importances_for_this_call": importances
        }
    except NotImplementedError as e:
        # Re-raise the missing spec error intentionally
        raise e
    except Exception as e:
        print(f"Error scoring with RF model: {e}")
        return {
            "eligible_probability": 0.0,
            "feature_importances_for_this_call": {}
        }
