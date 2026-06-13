import logging
from typing import List, Dict, Any

logger = logging.getLogger("voidmap.engine.counterfactual")
logging.basicConfig(level=logging.INFO)

class CounterfactualEngine:
    """
    VOIDMAP Counterfactual & Consequence Engine.
    Simulates alternative worlds and recalculates risk bounds based on adjustable variables.
    """
    @staticmethod
    def generate_scenarios(domain: str, missing_names: List[str]) -> List[Dict[str, Any]]:
        """
        Creates domain-specific alternative realities and dynamic shock scenarios.
        """
        scenarios = []
        missing_set = set(missing_names)
        
        # 1. Healthcare Scenarios
        if domain == "Healthcare":
            # Scenario A: Regulatory Tightening
            base_prob = 0.65
            base_impact = 7
            if "FDA / CE Regulatory Pathway" in missing_set:
                base_impact = 9
                base_prob = 0.85
                
            scenarios.append({
                "id": "cf-hc-reg",
                "name": "Federal FDA Regulatory Audit Tightening",
                "trigger_parameter": "regulatory_severity",
                "probability": base_prob,
                "base_impact": base_impact,
                "description": "Federal healthcare authorities impose mandatory software audits and double documentation compliance checks on active SaMD diagnostic platforms.",
                "consequence": "Project is forced to pause operations for expensive multi-year clinical trials if regulatory pathway nodes are absent."
            })
            
            # Scenario B: Hardware Drift / Calibration
            drift_impact = 5
            drift_prob = 0.50
            if "Clinical Drift Monitoring" in missing_set:
                drift_impact = 8
                drift_prob = 0.75
                
            scenarios.append({
                "id": "cf-hc-drift",
                "name": "Hardware Scanner Sensor Degradation (15%)",
                "trigger_parameter": "scanner_degradation",
                "probability": drift_prob,
                "base_impact": drift_impact,
                "description": "Hospital scanner sensors degrade or experience pixel artifacts due to maintenance delays or old hardware calibrations.",
                "consequence": "Without active data-drift checking, CNN model accuracy will collapse silently in production, misdiagnosing patient scans."
            })

        # 2. Cybersecurity Scenarios
        elif domain == "Cybersecurity":
            base_prob = 0.55
            base_impact = 6
            if "Threat Modeling" in missing_set:
                base_impact = 9
                base_prob = 0.80
                
            scenarios.append({
                "id": "cf-sec-auth",
                "name": "Credential Leak via Public Repository Commit",
                "trigger_parameter": "insider_vulnerability",
                "probability": base_prob,
                "base_impact": base_impact,
                "description": "A developer accidentally commits cloud administrative credential tokens in a public code repository.",
                "consequence": "Attackers hijack administrative dashboard databases immediately if credential shielding is not automated."
            })
            
            scenarios.append({
                "id": "cf-sec-ddos",
                "name": "Targeted Adversarial DDoS Evasion Attack",
                "trigger_parameter": "ddos_intensity",
                "probability": 0.60,
                "base_impact": 8 if "Adversarial Robustness Testing" in missing_set else 4,
                "description": "Hackers coordinate a DDoS wave combined with evasion perturbations designed to bypass normal classifiers.",
                "consequence": "System crashes or enters loop bypass states without adversarial robustness checking filters."
            })

        # 3. Startup / General Scenarios
        else:
            scale_impact = 5
            scale_prob = 0.60
            if "Infrastructure Scaling Model" in missing_set:
                scale_impact = 8
                scale_prob = 0.85
                
            scenarios.append({
                "id": "cf-st-scale",
                "name": "Sudden 100x Concurrency Spike",
                "trigger_parameter": "traffic_surge",
                "probability": scale_prob,
                "base_impact": scale_impact,
                "description": "A major technical blog features the product, driving a sudden 100x surge of active concurrent request transactions.",
                "consequence": "Infra charges spike exponentially, leading to server outages or runway exhaustion without a scaling model."
            })
            
            lic_impact = 4
            lic_prob = 0.50
            if "Regulatory Compliance Analysis" in missing_set:
                lic_impact = 8
                lic_prob = 0.70
                
            scenarios.append({
                "id": "cf-st-lic",
                "name": "State Operations Tax & Licensing Policy Change",
                "trigger_parameter": "regulatory_severity",
                "probability": lic_prob,
                "base_impact": lic_impact,
                "description": "Local state jurisdictions enact strict operational license requirements for digital software operators.",
                "consequence": "The platform is declared illegal, incurring massive retroactive fines and licensing shut-downs."
            })
            
        return scenarios

    @staticmethod
    def recalculate_risk_bounds(
        scenarios: List[Dict[str, Any]], 
        slider_values: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Dynamically adjusts probability and impact parameters based on slider changes (values 0.0 - 2.0).
        """
        updated_scenarios = []
        for sc in scenarios:
            param = sc["trigger_parameter"]
            multiplier = slider_values.get(param, 1.0)
            
            # Recalculate impact & probability with upper caps
            new_impact = min(10.0, float(sc["base_impact"] * multiplier))
            new_prob = min(1.0, float(sc["probability"] * (1.0 + (multiplier - 1.0) * 0.2)))
            
            # Determine dynamic counterfactual risk status
            risk_index = new_impact * new_prob
            if risk_index >= 7.0:
                status = "Critical"
            elif risk_index >= 4.5:
                status = "High"
            elif risk_index >= 2.0:
                status = "Moderate"
            else:
                status = "Low"
                
            updated_scenarios.append({
                "id": sc["id"],
                "name": sc["name"],
                "trigger_parameter": param,
                "probability": round(new_prob, 2),
                "base_impact": sc["base_impact"],
                "dynamic_impact": round(new_impact, 1),
                "risk_score": round(risk_index, 2),
                "status": status,
                "description": sc["description"],
                "consequence": sc["consequence"]
            })
        return updated_scenarios

counterfactual_engine = CounterfactualEngine()
