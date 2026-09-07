import numpy as np

def build_features(entities: dict, scheme: dict) -> np.ndarray:
    """
    takes accumulated_entities + a scheme's soft_features schema, 
    builds the exact feature vector the RF model expects.
    
    Per strict requirements: MUST GET THIS SPEC FROM USER, DO NOT GUESS IT.
    """
    raise NotImplementedError(
        "Feature schema has not been provided by the user. "
        "Cannot safely build the feature vector without knowing the exact column order and encodings "
        "the Random Forest model was trained on."
    )
