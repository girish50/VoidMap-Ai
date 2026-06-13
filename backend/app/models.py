from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    projects: List["Project"] = Relationship(back_populates="user")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str = Field(index=True, nullable=False)
    domain: str = Field(index=True, nullable=False) # e.g. Healthcare, Cybersecurity
    project_type: str = Field(nullable=False) # e.g. Medical AI, Cloud Platform
    risk_level: str = Field(default="Medium") # e.g. Low, Medium, High, Critical
    tech_stack: List[str] = Field(default=[], sa_column=Column(JSON))
    considered_factors: List[str] = Field(default=[], sa_column=Column(JSON))
    description: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="projects")
    analyses: List["Analysis"] = Relationship(back_populates="project")

class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", nullable=False)
    blindspot_score: float = Field(nullable=False) # Final aggregated score (e.g. 0-100)
    raw_text: str = Field(nullable=False)
    
    # Complex analysis results stored as JSON structures
    missing_factors: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    assumptions: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    failure_dna: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    counterfactuals: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    consequence_tree: Dict[str, Any] = Field(default={}, sa_column=Column(JSON)) # Nodes & Edges for React Flow
    
    # Advanced machine learning predictions
    threat_profile_class: Optional[str] = Field(default="Vulnerable")
    chain_fracture_probability: Optional[float] = Field(default=50.0)
    financial_liability_projection: Optional[float] = Field(default=500.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: Project = Relationship(back_populates="analyses")
    expert_reviews: List["ExpertReview"] = Relationship(back_populates="analysis")

class ExpertReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="analysis.id", nullable=False)
    expert_name: str = Field(nullable=False) # e.g. Red Team Attacker, SRE
    review_text: str = Field(nullable=False)
    rating: int = Field(default=5) # 1-10 scale
    categories: List[str] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    analysis: Analysis = Relationship(back_populates="expert_reviews")
