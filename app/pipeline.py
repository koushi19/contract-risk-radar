import joblib
import re
import os

# Load the model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.joblib')
model = joblib.load(MODEL_PATH)

def segment_clauses(text):
    """
    Splits contract into logical units.
    Rule: Clauses under 10 words merge with preceding clause.
    """
    # Split by common clause delimiters (newlines, or numbered patterns)
    raw_segments = re.split(r'\n+|(?:^|\s)\d+\.\s', text)
    raw_segments = [s.strip() for s in raw_segments if s.strip()]
    
    final_clauses = []
    for segment in raw_segments:
        word_count = len(segment.split())
        
        if final_clauses and word_count < 10:
            # Merge with preceding clause
            final_clauses[-1] = f"{final_clauses[-1]} {segment}"
        else:
            final_clauses.append(segment)
            
    return final_clauses

def get_reasoning(clause, label):
    """
    Generates a plain-English reasoning string based on clause content.
    """
    clause_lower = clause.lower()
    
    if label == "Risky":
        if "indemnify" in clause_lower and "no upper limit" in clause_lower:
            return "Uncapped indemnification — unilateral obligation with no liability ceiling."
        if "terminate" in clause_lower and "24 hours" in clause_lower:
            return "Extremely short termination notice period creates operational risk."
        if "uncapped" in clause_lower or "unlimited" in clause_lower:
            return "Contains 'uncapped' liability language which exposes the business to extreme risk."
        if "sole discretion" in clause_lower:
            return "Unilateral power granted to one party without objective criteria."
        return "Flags aggressive or one-sided legal terminology that requires legal review."
        
    elif label == "Review":
        if "renew" in clause_lower or "auto-renewal" in clause_lower:
            return "Automatic renewal present; requires tracking to avoid unwanted commitments."
        if "90 days" in clause_lower:
            return "Long notice period may limit flexibility to exit the agreement."
        if "arbitration" in clause_lower:
            return "Mandatory arbitration clause limits your right to seek court remedies."
        return "Contains terms that are not standard and should be manually verified."
        
    else: # Safe
        if "30 days" in clause_lower and "notice" in clause_lower:
            return "Standard mutual termination right with a reasonable notice period."
        if "confidential" in clause_lower:
            return "Standard confidentiality protection for shared information."
        return "Clause follows industry standard language and appears balanced."

def analyze_contract(text):
    """
    Main pipeline to process a contract.
    """
    clauses = segment_clauses(text)
    
    # Requirement: Minimum 3 clauses required
    if len(clauses) < 3:
        raise ValueError("Contract is too short. Minimum 3 logical clauses are required for analysis.")
    
    results = []
    risk_counts = {"Safe": 0, "Review": 0, "Risky": 0}
    
    for i, clause_text in enumerate(clauses):
        # Predict
        prediction = model.predict([clause_text])[0]
        # Get confidence score (probability)
        probs = model.predict_proba([clause_text])[0]
        confidence = max(probs)
        
        # Truncate for display (Max 300 chars)
        display_text = (clause_text[:297] + '...') if len(clause_text) > 300 else clause_text
        
        reasoning = get_reasoning(clause_text, prediction)
        
        results.append({
            "number": i + 1,
            "text": display_text,
            "label": prediction,
            "confidence": round(float(confidence), 2),
            "reasoning": reasoning
        })
        
        risk_counts[prediction] += 1
        
    # Find top 3 highest-risk clauses by confidence
    # Filter for Risky first, then Review, then Safe
    sorted_by_risk = sorted(results, key=lambda x: (
        1 if x['label'] == 'Risky' else (2 if x['label'] == 'Review' else 3),
        -x['confidence']
    ))
    top_3 = sorted_by_risk[:3]
    
    summary = {
        "total_clauses": len(clauses),
        "risk_distribution": risk_counts,
        "top_3": top_3
    }
    
    return summary, results
