import logging
from typing import List, Dict, Any
from app.graph_db import graph_db
from app.engines.nlp_helper import extract_entities_and_technologies

logger = logging.getLogger("voidmap.engine.absence")
logging.basicConfig(level=logging.INFO)

class AbsenceReasoningEngine:
    """
    VOIDMAP Absence Reasoning Engine.
    Detects what the system builder forgot to consider based on expectations stored in the graph.
    """
    @staticmethod
    def analyze_gaps(domain: str, proposal_text: str, user_considered: List[str]) -> Dict[str, Any]:
        """
        Runs absence reasoning logic by comparing expected nodes against extracted keywords.
        """
        logger.info(f"Running Absence Reasoning for domain: {domain}")
        
        # 1. Fetch expected requirements from the Knowledge Graph (Neo4j / NetworkX)
        expected_requirements = graph_db.get_domain_requirements(domain)
        if not expected_requirements:
            logger.warning(f"No expectation nodes found for domain: {domain}. Returning empty analysis.")
            return {
                "coverage_score": 100.0,
                "missing_factors": [],
                "considered_factors": list(user_considered)
            }
            
        # 2. Extract considerations mentioned in the text
        extracted_data = extract_entities_and_technologies(proposal_text)
        nlp_considerations = extracted_data["considerations"]
        
        # Normalize all considerations (lowercase, trimmed) to avoid case mismatches
        all_considerations = set(c.lower().strip() for c in user_considered)
        for c in nlp_considerations:
            all_considerations.add(c.lower().strip())
            
        missing_factors = []
        covered_count = 0
        total_count = len(expected_requirements)
        
        # 3. Mismatch check
        for req in expected_requirements:
            req_name = req["requirement"]
            category = req["category"]
            description = req["description"]
            risk = req["risk"]
            dependencies = req.get("dependencies", [])
            
            # Simple keyword search inside proposal text as a fallback
            req_normalized = req_name.lower().strip()
            text_mentions_req = req_normalized in proposal_text.lower()
            
            is_considered = False
            # Check if any user factor matches or NLP extracted term is closely related
            for item in all_considerations:
                if item in req_normalized or req_normalized in item:
                    is_considered = True
                    break
                    
            if is_considered or text_mentions_req:
                covered_count += 1
            else:
                # Flag as missing factor
                missing_factors.append({
                    "requirement": req_name,
                    "category": category,
                    "description": description,
                    "risk": risk,
                    "dependencies": dependencies,
                    "fractured_chain": False # Handled in dependency step
                })
                
        # 4. Dependency Chain Fracture analysis
        # If a dependency of a covered node is missing, mark the covered node as "fractured"
        missing_names = {item["requirement"] for item in missing_factors}
        for item in missing_factors:
            for dep in item["dependencies"]:
                if dep in missing_names:
                    item["fractured_chain"] = True
                    
        # 5. Compute Coverage Score (percentage)
        coverage_score = (covered_count / total_count) * 100.0 if total_count > 0 else 100.0
        
        return {
            "coverage_score": round(coverage_score, 1),
            "missing_factors": missing_factors,
            "total_expected_count": total_count,
            "covered_count": covered_count
        }

absence_engine = AbsenceReasoningEngine()
