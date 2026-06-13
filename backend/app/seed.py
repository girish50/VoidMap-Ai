import json
import logging
from sqlmodel import Session, select
from app import database as db
from app.models import User, Project, Analysis, ExpertReview
from app.graph_db import graph_db

logger = logging.getLogger("voidmap.seed")
logging.basicConfig(level=logging.INFO)

def seed_relational_database(session: Session):
    """
    Seeds the PostgreSQL / SQLite database with a default developer user,
    default project submissions, and rich historical analysis dashboards.
    """
    logger.info("Checking relational database tables...")
    
    # 1. Check if default user exists
    db_user = session.exec(select(User).where(User.username == "void_developer")).first()
    if not db_user:
        logger.info("Creating default developer user: void_developer")
        db_user = User(
            username="void_developer",
            hashed_password="pbkdf2_sha256$120000$hashedpasswordstringvalue123" # Secure placeholder
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    
    # 2. Check if default projects exist
    existing_project = session.exec(select(Project)).first()
    if not existing_project:
        logger.info("Seeding relational database with clinical medical AI case study...")
        
        # Clinical Diagnostic Project
        project1 = Project(
            user_id=db_user.id,
            name="AlphaMed Chest X-Ray CNN",
            domain="Healthcare",
            project_type="Medical AI",
            risk_level="High",
            tech_stack=["React", "FastAPI", "PyTorch", "Docker", "AWS S3"],
            considered_factors=["Accuracy", "Cloud hosting", "User Interface"],
            description="A high-performance convolutional neural network trained on public clinical datasets to classify chest X-ray images for lung diseases like pneumonia and tuberculosis, providing direct visual attention heatmaps to radiologist terminals."
        )
        session.add(project1)
        session.commit()
        session.refresh(project1)
        
        # Analysis results
        analysis1 = Analysis(
            project_id=project1.id,
            blindspot_score=78.5,
            raw_text=project1.description,
            missing_factors=[
                {
                    "requirement": "Clinical Validation",
                    "category": "Compliance",
                    "description": "Rigorous clinical trials or validation against gold-standard manual diagnostic reviews.",
                    "risk": "Inaccurate predictions resulting in patient harm, misdiagnosis liability, and regulatory rejection."
                },
                {
                    "requirement": "Demographic Bias Mitigation",
                    "category": "Ethics",
                    "description": "Evaluation of model accuracy across diverse ages, genders, ethnicities, and socio-economic groups.",
                    "risk": "Systemic bias resulting in unequal care quality and civil rights compliance breaches."
                },
                {
                    "requirement": "FDA / CE Regulatory Pathway",
                    "category": "Legal",
                    "description": "Regulatory filings, audits, and approvals for software as a medical device (SaMD).",
                    "risk": "Illegal distribution charges, heavy fines, and immediate system cease-and-desist orders."
                }
            ],
            assumptions=[
                {
                    "claim": "Trained on public clinical datasets",
                    "assumption": "The public clinical datasets represent the real demographic and scanning calibrations of our target deployment hospitals.",
                    "vulnerability": "Scanner variance (low-quality vs high-quality machines) and patient demographic shifts will cause accuracy to collapse in real deployment.",
                    "rating": 8
                }
            ],
            failure_dna=[
                {
                    "archetype": "Theranos Diagnostic Meltdown",
                    "similarity": 0.82,
                    "summary": "Exaggeration of blood testing automation capabilities without clinical validation. Circumvented FDA pathways and operated in complete diagnostic secrecy."
                },
                {
                    "archetype": "IBM Watson Health Oncology Failure",
                    "similarity": 0.74,
                    "summary": "Watson Oncology was trained on small, synthetic cohorts from a single cancer center rather than real patient datasets. When deployed globally, it recommended dangerous and incorrect treatments due to data mismatches."
                }
            ],
            counterfactuals=[
                {
                    "scenario": "FDA imposes strict SaaS Medical Device audit regulations",
                    "base_risk": "Moderate",
                    "scaled_risk": "Critical",
                    "probability": 0.85,
                    "impact": "Project requires complete multi-year shutdown for clinical trials, causing immediate operational collapse."
                },
                {
                    "scenario": "Scanning hardware experiences 15% sensor degradation or noise",
                    "base_risk": "Low",
                    "scaled_risk": "High",
                    "probability": 0.70,
                    "impact": "Model accuracy drops from 95% to 62%, misdiagnosing dozens of patients silently."
                }
            ],
            consequence_tree={
                "nodes": [
                    {"id": "n1", "type": "input", "data": {"label": "Deploy CNN to Clinical Cloud"}, "position": {"x": 250, "y": 20}},
                    {"id": "n2", "data": {"label": "Unvalidated Scanner Mismatches"}, "position": {"x": 100, "y": 120}},
                    {"id": "n3", "data": {"label": "FDA SaMD Liability Audit"}, "position": {"x": 400, "y": 120}},
                    {"id": "n4", "type": "output", "data": {"label": "Silent Misdiagnoses & Malpractice Suits"}, "position": {"x": 100, "y": 240}},
                    {"id": "n5", "type": "output", "data": {"label": "Immediate Cease-and-Desist Order"}, "position": {"x": 400, "y": 240}}
                ],
                "edges": [
                    {"id": "e1", "source": "n1", "target": "n2"},
                    {"id": "e2", "source": "n1", "target": "n3"},
                    {"id": "e3", "source": "n2", "target": "n4"},
                    {"id": "e4", "source": "n3", "target": "n5"}
                ]
            }
        )
        session.add(analysis1)
        session.commit()
        session.refresh(analysis1)
        
        # Expert boardroom critiques
        expert1 = ExpertReview(
            analysis_id=analysis1.id,
            expert_name="Compliance Officer",
            review_text="This healthcare project is highly vulnerable due to the complete lack of an FDA/CE clearance pathway. Distributing neural network diagnostic advice without medical device audits carries massive criminal liability and civil malpractice risks.",
            rating=9,
            categories=["Regulatory", "Legal", "Liability"]
        )
        expert2 = ExpertReview(
            analysis_id=analysis1.id,
            expert_name="System Reliability Engineer",
            review_text="While Docker and AWS are outlined, there is no mention of scanner-drift monitoring. Scanners change calibrations constantly, and neural networks are extremely sensitive to noise. Without a robust data-drift checking suite, accuracy will silently degrade in production.",
            rating=6,
            categories=["Operations", "Data Quality", "Scalability"]
        )
        expert3 = ExpertReview(
            analysis_id=analysis1.id,
            expert_name="Red Team Attacker",
            review_text="Public cloud hosting with a standard API is highly susceptible to model extraction attacks and adversarial perturbations. An attacker can tweak a few pixels of a healthy lung X-ray to force a tuberculosis diagnosis, potentially manipulating clinical insurance billing schemas.",
            rating=7,
            categories=["Security", "Exploitation", "Adversarial"]
        )
        session.add(expert1)
        session.add(expert2)
        session.add(expert3)
        session.commit()
        
        logger.info("Successfully seeded SQL database with clinical mock data.")

def main():
    logger.info("Starting database seeding process...")
    # Initialize schema
    db.create_db_and_tables()
    
    # Seed Relational DB
    with Session(db.engine) as session:
        seed_relational_database(session)
        
    # Seed Graph DB (Neo4j)
    if graph_db.is_connected:
        logger.info("Seeding Neo4j Graph Database nodes and relations...")
        graph_db.seed_graph_database()
    else:
        logger.info("Neo4j database offline. In-memory NetworkX model is pre-populated and ready for fallbacks.")
        
    logger.info("VOIDMAP AI database initialization complete.")

if __name__ == "__main__":
    main()
