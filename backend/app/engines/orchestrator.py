import logging
import numpy as np
from typing import List, Dict, Any

# Core Engines Imports
from app.engines.absence import absence_engine
from app.engines.assumptions import assumption_attack_engine
from app.engines.experts import expert_ecosystem_engine
from app.engines.counterfactual import counterfactual_engine
from app.engines.failure_dna import failure_dna_mapper
from app.engines.consequence import consequence_tree_generator

logger = logging.getLogger("voidmap.engine.orchestrator")
logging.basicConfig(level=logging.INFO)

# Attempt to load Scikit-Learn tools for relational predictive regressions
ML_FALLBACK_ACTIVE = False
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.svm import SVC
    logger.info("Scikit-Learn ML Engines (RF, DT, Linear, Logistic, SVM) successfully imported.")
except Exception as e:
    logger.warning(f"Could not load Scikit-Learn modules ({e}). Activating lightweight mathematical model fallbacks.")
    ML_FALLBACK_ACTIVE = True

class ReasoningOrchestrator:
    """
    VOIDMAP Reasoning Orchestrator.
    Executes and binds all six intelligence engines into a unified pipeline.
    """
    @staticmethod
    def execute_analysis(
        project_name: str,
        domain: str,
        project_type: str,
        risk_level: str,
        tech_stack: List[str],
        considered_factors: List[str],
        proposal_text: str
    ) -> Dict[str, Any]:
        """
        Runs the complete execution pipeline (Frontend -> NLP -> Graph -> ML -> Experts -> Consequence Tree -> Output).
        """
        global ML_FALLBACK_ACTIVE
        logger.info(f"Initiating end-to-end VOIDMAP reasoning pipeline for: {project_name}")
        
        # 1. Run Absence Reasoning Engine (Knowledge Graph Set-Diff)
        absence_results = absence_engine.analyze_gaps(domain, proposal_text, considered_factors)
        coverage_score = absence_results["coverage_score"]
        missing_factors = absence_results["missing_factors"]
        
        # Compile list of missing requirement names
        missing_names = [m["requirement"] for m in missing_factors]
        
        # 2. Run Assumption Attack Engine (Claim Parsing & Fragility scoring)
        assumptions = assumption_attack_engine.analyze_assumptions(proposal_text, domain)
        avg_fragility = 5.0
        if assumptions:
            avg_fragility = sum(a["fragility_score"] for a in assumptions) / len(assumptions)
            
        # 3. Run Failure DNA Mapper (Cosine similarity & corporate collapses matching)
        failure_dna_matches = failure_dna_mapper.map_failure_dna(proposal_text, domain, missing_names)
        highest_similarity = 0.0
        if failure_dna_matches:
            highest_similarity = failure_dna_matches[0]["similarity"]
            
        # 4. Run Multi-Perspective Expert Boardroom Critique Engine
        expert_board_results = expert_ecosystem_engine.generate_expert_reviews(domain, proposal_text, missing_factors)
        
        # 5. Run Counterfactual Engine (Scenario generators)
        scenarios = counterfactual_engine.generate_scenarios(domain, missing_names)
        
        # 6. Run Consequence Ripple Tree Generator (React Flow Nodes & Edges)
        consequence_tree = consequence_tree_generator.generate_tree(project_name, domain, missing_names)
        
        # ----------------------------------------------------
        # MACHINE LEARNING PREDICTIVE SUITE (Scikit-Learn)
        # ----------------------------------------------------
        final_blindspot_score = 0.0
        predicted_complexity_growth = 0.0
        threat_profile_class = "Vulnerable"
        chain_fracture_probability = 50.0
        financial_liability_projection = 500.0
        
        if not ML_FALLBACK_ACTIVE:
            try:
                # Dynamic training dataset representing known system configurations
                # Features: [Coverage Score, Avg Assumption Fragility, Max Failure Similarity]
                training_x = np.array([
                    [100.0, 1.0, 0.00], # Case 1: Resilient system
                    [80.0,  3.0, 0.20], # Case 2: Minor gaps, low fragility
                    [60.0,  5.0, 0.45], # Case 3: Moderate gaps
                    [30.0,  8.0, 0.70], # Case 4: Severe gaps, high fragility
                    [0.0,  10.0, 0.95]  # Case 5: Empty specifications
                ])
                
                # Labels for supervised predictions:
                # 1. Random Forest (Blindspot Risk score: 0-100)
                labels_risk = np.array([5.0, 25.0, 52.0, 78.0, 98.0])
                
                # 2. Decision Tree (Maintenance Complexity growth: 10-120%)
                labels_complexity = np.array([10.0, 30.0, 55.0, 85.0, 120.0])
                
                # 3. Support Vector Machine (SVC Threat Classification: 0=Resilient, 1=Vulnerable, 2=Critical)
                labels_threat = np.array([0, 0, 1, 1, 2])
                
                # 4. Logistic Regression (Binary Chain Fracture class: 0=Safe, 1=Fractured)
                labels_fracture = np.array([0, 0, 0, 1, 1])
                
                # 5. Linear Regression (Financial Risk Liability cost projection in $ Thousands)
                labels_liability = np.array([20.0, 120.0, 500.0, 1200.0, 2500.0])
                
                # Fit standard RandomForestRegressor for final Blindspot Score
                rf_regressor = RandomForestRegressor(n_estimators=10, random_state=42)
                rf_regressor.fit(training_x, labels_risk)
                
                # Fit DecisionTreeRegressor for explainable Complexity growth
                dt_regressor = DecisionTreeRegressor(random_state=42)
                dt_regressor.fit(training_x, labels_complexity)
                
                # Fit SVM Support Vector Classifier (SVC) for Threat Profile
                svm_classifier = SVC(probability=True, random_state=42)
                svm_classifier.fit(training_x, labels_threat)
                
                # Fit Logistic Regression Classifier for Chain Fracture probability
                log_regressor = LogisticRegression(random_state=42)
                log_regressor.fit(training_x, labels_fracture)
                
                # Fit Linear Regression Regressor for Financial Liability cost projection
                linear_regressor = LinearRegression()
                linear_regressor.fit(training_x, labels_liability)
                
                # Predict for current project features
                test_sample = np.array([[float(coverage_score), float(avg_fragility), float(highest_similarity)]])
                
                final_blindspot_score = float(rf_regressor.predict(test_sample)[0])
                predicted_complexity_growth = float(dt_regressor.predict(test_sample)[0])
                
                threat_id = int(svm_classifier.predict(test_sample)[0])
                threat_profile_class = ["Resilient", "Vulnerable", "Critical"][threat_id]
                
                fracture_probs = log_regressor.predict_proba(test_sample)[0]
                chain_fracture_probability = float(fracture_probs[1] * 100.0)
                
                financial_liability_projection = float(linear_regressor.predict(test_sample)[0])
                
            except Exception as e:
                logger.warning(f"Scikit-Learn predictive suite fitting failed ({e}). Activating fallbacks.")
                ML_FALLBACK_ACTIVE = True
                
        if ML_FALLBACK_ACTIVE:
            # Fallback mathematical models matching same curves
            base_blindspot = 100.0 - coverage_score
            fragility_overhead = avg_fragility * 2.8
            dna_overhead = highest_similarity * 15.0
            
            final_blindspot_score = base_blindspot + fragility_overhead + dna_overhead
            predicted_complexity_growth = (100.0 - coverage_score) * 1.1 + (avg_fragility * 2.0)
            
            if final_blindspot_score >= 70:
                threat_profile_class = "Critical"
                chain_fracture_probability = 85.0
            elif final_blindspot_score >= 40:
                threat_profile_class = "Vulnerable"
                chain_fracture_probability = 45.0
            else:
                threat_profile_class = "Resilient"
                chain_fracture_probability = 15.0
                
            financial_liability_projection = final_blindspot_score * 25.0
            
        # Clamp results strictly to target bounds
        final_blindspot_score = max(0.0, min(100.0, round(final_blindspot_score, 1)))
        predicted_complexity_growth = max(10.0, min(150.0, round(predicted_complexity_growth, 1)))
        chain_fracture_probability = max(0.0, min(100.0, round(chain_fracture_probability, 1)))
        financial_liability_projection = max(5.0, round(financial_liability_projection, 1))
        
        logger.info(f"VOIDMAP pipeline execution complete. Calculated Blindspot Score: {final_blindspot_score}%")
        
        return {
            "project_name": project_name,
            "domain": domain,
            "project_type": project_type,
            "risk_level": risk_level,
            "tech_stack": tech_stack,
            "considered_factors": considered_factors,
            "coverage_score": coverage_score,
            "blindspot_score": final_blindspot_score,
            "predicted_complexity_growth": predicted_complexity_growth,
            "threat_profile_class": threat_profile_class,
            "chain_fracture_probability": chain_fracture_probability,
            "financial_liability_projection": financial_liability_projection,
            "missing_factors": missing_factors,
            "assumptions": assumptions,
            "failure_dna": failure_dna_matches[:3], 
            "expert_reviews": expert_board_results["expert_reviews"],
            "board_disagreements": expert_board_results["board_disagreements"],
            "counterfactuals": scenarios,
            "consequence_tree": consequence_tree
        }

reasoning_orchestrator = ReasoningOrchestrator()
