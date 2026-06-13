import logging
from typing import List, Dict, Any

logger = logging.getLogger("voidmap.engine.experts")
logging.basicConfig(level=logging.INFO)

class ExpertEcosystemEngine:
    """
    VOIDMAP Multi-Perspective Adversarial Expert Ecosystem Engine.
    Generates rich boardroom debates, critiques, risk levels, and clashes.
    """
    @staticmethod
    def generate_expert_reviews(
        domain: str, 
        proposal_text: str, 
        missing_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesizes adversarial reviews from diverse personas based on the project's identified gaps.
        """
        logger.info(f"Synthesizing expert boardroom review for domain: {domain}")
        
        missing_names = {m["requirement"] for m in missing_factors}
        reviews = []
        
        # ----------------------------------------------------
        # PERSONA 1: COMPLIANCE OFFICER & LEGAL COUNSEL
        # ----------------------------------------------------
        comp_rating = 4
        comp_critique = "From a regulatory perspective, this proposal lacks explicit operational guardrails. "
        
        if "FDA / CE Regulatory Pathway" in missing_names or "Clinical Validation" in missing_names:
            comp_rating = 9
            comp_critique += (
                "The complete omission of clinical trial validation and an FDA SaMD compliance pathway is a critical blocker. "
                "Distributing diagnostic software without federal audit reviews introduces severe class-action malpractice liability."
            )
        elif "Patient Privacy & HIPAA" in missing_names or "KYC / AML Regulatory Integration" in missing_names:
            comp_rating = 8
            comp_critique += (
                "Omission of formal privacy de-identification protocols introduces HIPAA or GDPR compliance fines. "
                "State-level regulators will mandate an immediate cease-and-desist order upon discovery."
            )
        else:
            comp_critique += "The compliance risk is moderate, but ensure clear document audit logging is active for standard liability protection."
            
        reviews.append({
            "expert_name": "Compliance Officer",
            "rating": comp_rating,
            "categories": ["Legal", "Regulatory", "Liability"],
            "critique": comp_critique
        })

        # ----------------------------------------------------
        # PERSONA 2: RED TEAM ATTACKER (SECURITY ENGINEER)
        # ----------------------------------------------------
        sec_rating = 4
        sec_critique = "Architecturally, the threat boundaries are poorly defined. "
        
        if "Threat Modeling" in missing_names or "Secrets and Credentials Shielding" in missing_names:
            sec_rating = 9
            sec_critique += (
                "Deploying this system without rigorous STRIDE threat modeling is a critical vulnerability. "
                "Any public API endpoint without rate-limiting circuit breakers is trivial to crash. "
                "Hardcoded credentials in public git repositories will lead to immediate cloud control panel hijack."
            )
        elif "Key Lifecycle Management" in missing_names or "Adversarial Robustness Testing" in missing_names:
            sec_rating = 8
            sec_critique += (
                "No mention of adversarial robustness testing allows hackers to bypass filters with minimal perturbed samples. "
                "Unrotated database keys will leak, compromising all data stores."
            )
        else:
            sec_critique += "Standard firewall protections are present, but implement active API token rotations to mitigate lateral escalations."

        reviews.append({
            "expert_name": "Red Team Attacker",
            "rating": sec_rating,
            "categories": ["Security", "Vulnerability", "Exploitation"],
            "critique": sec_critique
        })

        # ----------------------------------------------------
        # PERSONA 3: SYSTEM RELIABILITY ENGINEER (SRE)
        # ----------------------------------------------------
        sre_rating = 4
        sre_critique = "From a reliability viewpoint, the infrastructure deployment lacks resilience metrics. "
        
        if "Load Testing & Scalability" in missing_names or "Disaster Recovery Strategy" in missing_names:
            sre_rating = 8
            sre_critique += (
                "Launching without rigorous load testing will lead to instant server saturation. "
                "If AWS experiences a single regional outage, the complete lack of dual-active replication means indefinite user downtime."
            )
        elif "Clinical Drift Monitoring" in missing_names or "Database Drift & Schema Migrations" in missing_names:
            sre_rating = 7
            sre_critique += (
                "Failing to monitor input drift is highly risky. Sensor drift will silently compromise predictions, "
                "and executing schema migrations manually on live databases will corrupt tabular relational states."
            )
        else:
            sre_critique += "Dockerization provides good portability. Focus on establishing auto-scaling triggers to handle request spikes."

        reviews.append({
            "expert_name": "System Reliability Engineer",
            "rating": sre_rating,
            "categories": ["Operations", "Resilience", "Infrastructure"],
            "critique": sre_critique
        })

        # ----------------------------------------------------
        # PERSONA 4: VENTURE CAPITAL INVESTOR
        # ----------------------------------------------------
        inv_rating = 3
        inv_critique = "As a business strategist, I evaluate scalable economics and time-to-market. "
        
        if "Customer Acquisition Cost Audit" in missing_names or "Infrastructure Scaling Model" in missing_names:
            inv_rating = 8
            inv_critique += (
                "The startup unit economics are completely unproven. If server maintenance cost grows exponentially "
                "with user acquisition, scaling up will bleed capital rapidly, exhausting our runway before seed funding."
            )
        elif "IP and Patent Strategy" in missing_names:
            inv_rating = 7
            inv_critique += (
                "Lack of proprietary IP patents makes this easy to replicate. Large cloud giants can easily clone "
                "your open architecture, neutralizing your market lead in under six months."
            )
        else:
            inv_critique += "The core concept holds strong market fit. Ensure infrastructure costs stay linear to protect profit margins."

        reviews.append({
            "expert_name": "VC Investor",
            "rating": inv_rating,
            "categories": ["Finance", "Strategy", "IP Strategy"],
            "critique": inv_critique
        })

        # ----------------------------------------------------
        # PERSONA 5: ETHICIST & HUMAN FACTORS EXPERT
        # ----------------------------------------------------
        eth_rating = 3
        eth_critique = "The societal and human feedback loops are largely neglected. "
        
        if "Demographic Bias Mitigation" in missing_names or "Equity Impact Assessment" in missing_names:
            eth_rating = 8
            eth_critique += (
                "Training models exclusively on public datasets without demographic bias testing is highly unethical. "
                "Accuracy rates will drop dramatically for minority age or racial brackets, perpetuating systemic health/policy inequality."
            )
        elif "Explainability & Interpretability" in missing_names or "Public Accountability Protocol" in missing_names:
            eth_rating = 7
            eth_critique += (
                "Clinicians will blindly trust or completely reject the AI due to a lack of visual explanation. "
                "Public users need transparent channels to dispute automated decisions."
            )
        else:
            eth_critique += "Basic privacy protections exist. Implement human-in-the-loop oversight to audit model advice."

        reviews.append({
            "expert_name": "Ethicist",
            "rating": eth_rating,
            "categories": ["Ethics", "Bias", "Explainability"],
            "critique": eth_critique
        })

        # ----------------------------------------------------
        # BOARD DISAGREEMENTS & CONFLICT ENGINES
        # ----------------------------------------------------
        disagreements = []
        
        # Conflict A: Speed vs. Compliance
        if comp_rating >= 7 and inv_rating >= 6:
            disagreements.append({
                "clash": "Time-to-Market vs. Regulatory Safety",
                "dialogue": (
                    "The VC Investor urges: 'We need to launch our prototype immediately to secure seed capital!' "
                    "The Compliance Officer fires back: 'Launching without clinical validation and SaMD approvals is illegal. "
                    "One regulatory cease-and-desist or patient lawsuit will instantly destroy the brand equity!'"
                )
            })
            
        # Conflict B: Security Overhead vs. Resource Cost
        if sec_rating >= 7 and inv_rating >= 6:
            disagreements.append({
                "clash": "Security Engineering vs. Burn Rate",
                "dialogue": (
                    "The Red Team Attacker demands: 'We must dedicate two developer cycles to threat modeling, API encryption, and HSM key rotation.' "
                    "The VC Investor responds: 'Over-engineering security on a pre-revenue codebase slows delivery speed and increases server overhead unnecessarily.'"
                )
            })
            
        # Conflict C: Scalability vs. Budget
        if sre_rating >= 7 and inv_rating >= 5:
            disagreements.append({
                "clash": "Multi-Region Redundancy vs. Operating Expenses",
                "dialogue": (
                    "The SRE insists: 'We need redundant multi-region server clusters to maintain 99.9% uptime.' "
                    "The VC Investor objects: 'Our infra scaling model doesn't support dual-active AWS hosting. "
                    "Our customer acquisition budget cannot survive high monthly infrastructure overhead!'"
                )
            })

        if not disagreements:
            # Default fallback boardroom discussion
            disagreements.append({
                "clash": "Operational Scaling vs. Execution Cost",
                "dialogue": (
                    "The VC Investor asks: 'How quickly can we acquire 10,000 active users?' "
                    "The SRE warns: 'Not before we run comprehensive load testing and drift monitoring. "
                    "Without SRE audits, a traffic surge will bring down the server, causing instant user attrition.'"
                )
            })
            
        return {
            "expert_reviews": reviews,
            "board_disagreements": disagreements
        }

expert_ecosystem_engine = ExpertEcosystemEngine()
