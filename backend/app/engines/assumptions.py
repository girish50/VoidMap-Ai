import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger("voidmap.engine.assumptions")
logging.basicConfig(level=logging.INFO)

class AssumptionAttackEngine:
    """
    VOIDMAP Assumption Attack Engine.
    Extracts silent/implicit assumptions from user proposals and stress-tests them with threat vectors.
    """
    @staticmethod
    def analyze_assumptions(proposal_text: str, domain: str) -> List[Dict[str, Any]]:
        """
        Parses text for claims using regex sentence tokenization, matches threat models,
        and computes an index of claim fragility.
        """
        logger.info(f"Extracting implicit assumptions for domain: {domain}")
        
        # Simple regex sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', proposal_text)
        extracted_assumptions = []
        
        # Define assertion linguistic indicators
        patterns = [
            (r"\b(will|always|guarantee|never|perfect|100%|completely|fully|highly)\b", "Absolute Assertion"),
            (r"\b(accuracy|performance|efficient|fast|optimal)\b", "Performance Overconfidence"),
            (r"\b(secure|encrypted|safe|protected|unbreakable)\b", "Security Solved Assumption"),
            (r"\b(public dataset|dataset|data source|clean data)\b", "Data Generalization Claim"),
            (r"\b(we assume|assuming|assumed)\b", "Explicit Assumption")
        ]
        
        for idx, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
                
            matched_type = None
            matched_word = None
            
            # Check linguistic rules
            for regex, claim_type in patterns:
                match = re.search(regex, sentence.lower())
                if match:
                    matched_type = claim_type
                    matched_word = match.group(0)
                    break
                    
            if matched_type:
                # Calculate Base Fragility (1-10 scale)
                base_fragility = 5
                
                # Accents that increase fragility
                if matched_type == "Absolute Assertion":
                    base_fragility += 2
                if matched_type == "Security Solved Assumption":
                    base_fragility += 1
                    
                # Domain multiplier adjustments
                domain_multiplier = 1.0
                if domain in ("Healthcare", "Cybersecurity", "Finance"):
                    domain_multiplier = 1.3
                    base_fragility += 1
                elif domain in ("Policy", "Infrastructure"):
                    domain_multiplier = 1.15
                    base_fragility += 1
                    
                final_fragility = min(10, int(base_fragility * domain_multiplier))
                
                # Derive targeted adversarial attacks based on indicators
                attack_question = ""
                vulnerability = ""
                
                if matched_type == "Absolute Assertion":
                    attack_question = f"What fails when a situation occurs where the system CANNOT '{matched_word}' deliver this behavior?"
                    vulnerability = "Fragility to extreme outliers and black-swan edge cases."
                elif matched_type == "Performance Overconfidence":
                    attack_question = "How does accuracy degrade if network latency increases 10x or scanning resolution drops by half?"
                    vulnerability = "Sensitivity to variable execution environment and network lag."
                elif matched_type == "Security Solved Assumption":
                    attack_question = "What happens if a authenticated user is compromised internally, or a malicious actor poisons the pipeline?"
                    vulnerability = "Vulnerability to credential theft and insider server access."
                elif matched_type == "Data Generalization Claim":
                    attack_question = "How will the system adapt when real-world user distributions drift 30% away from this training dataset?"
                    vulnerability = "Susceptibility to out-of-distribution drift and selection bias."
                else:
                    attack_question = "What empirical evidence supports this assumption, and what is the recovery protocol if it fails?"
                    vulnerability = "Lack of fallback architecture if the core premise collapses."
                    
                extracted_assumptions.append({
                    "id": f"as-{idx}",
                    "claim": sentence,
                    "type": matched_type,
                    "vulnerability": vulnerability,
                    "attack_question": attack_question,
                    "fragility_score": final_fragility
                })
                
        # If no linguistic assumptions matched, provide a standard default domain assumption to prevent empty lists
        if not extracted_assumptions:
            default_assumptions = {
                "Healthcare": {
                    "claim": "We assume our neural diagnostic models perform consistently across clinical settings.",
                    "type": "Generalization Assumption",
                    "vulnerability": "Vulnerability to local hospital scanner hardware variance.",
                    "attack_question": "How will you calibrate the models when a rural hospital uploads low-resolution scans?",
                    "fragility_score": 7
                },
                "Cybersecurity": {
                    "claim": "We assume our access control shielding holds against concurrent DDoS injection attacks.",
                    "type": "Security Resilience Assumption",
                    "vulnerability": "Fragility to zero-day concurrency vulnerabilities.",
                    "attack_question": "What is the physical rate-limiting cutoff threshold to prevent buffer-overflow bypasses?",
                    "fragility_score": 8
                }
            }
            default = default_assumptions.get(domain, {
                "claim": "We assume our operating resources and server stack scale linearly without performance blockages.",
                "type": "Operational Resource Assumption",
                "vulnerability": "Risk of server resource saturation.",
                "attack_question": "How does the system handle a sudden 100x user spike in under 60 seconds?",
                "fragility_score": 6
            })
            extracted_assumptions.append(default)
            
        return extracted_assumptions

assumption_attack_engine = AssumptionAttackEngine()
