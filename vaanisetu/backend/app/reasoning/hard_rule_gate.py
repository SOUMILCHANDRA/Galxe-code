def evaluate_hard_constraints(entities: dict, schemes: list) -> list:
    """
    Evaluates extracted entities against scheme hard constraints.
    Returns a list of schemes that pass the hard constraints.
    """
    eligible_schemes = []
    
    user_age = entities.get("age", -1)
    if isinstance(user_age, str):
        try:
            user_age = int(user_age)
        except:
            user_age = -1
            
    user_occupation = str(entities.get("occupation", "")).lower()
    user_location = str(entities.get("location_type", "")).lower()
    user_docs = [doc.lower() for doc in entities.get("documents", [])]
    
    for scheme in schemes:
        constraints = scheme.get("hard_constraints", {})
        
        # Check age band
        age_min = constraints.get("age_min")
        age_max = constraints.get("age_max")
        if age_min is not None and user_age != -1 and user_age < age_min:
            continue
        if age_max is not None and user_age != -1 and user_age > age_max:
            continue
            
        # Check location type
        req_location = constraints.get("location_type")
        if req_location and user_location and req_location.lower() != user_location:
            continue
            
        # Check occupation categories
        req_occupations = constraints.get("occupation_categories", [])
        if req_occupations and user_occupation:
            match = False
            for occ in req_occupations:
                if occ.lower() in user_occupation:
                    match = True
                    break
            if not match:
                continue
                
        # Check mandatory documents
        req_docs = constraints.get("required_docs", [])
        if req_docs:
            has_all = True
            for req_doc in req_docs:
                if req_doc.lower() not in user_docs:
                    has_all = False
                    break
            if not has_all:
                continue
                
        eligible_schemes.append(scheme)
        
    return eligible_schemes
