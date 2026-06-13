import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

class Settings:
    # App General Settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # PostgreSQL Configuration with SQLite auto-fallback
    _raw_db_url = os.getenv("DATABASE_URL", "").strip()
    if _raw_db_url:
        DATABASE_URL: str = _raw_db_url
    else:
        # SQLite database file path in backend root
        sqlite_path = BASE_DIR / "voidmap.db"
        DATABASE_URL: str = f"sqlite:///{sqlite_path}"
        
    # Neo4j Configuration
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    
    # Fallback configuration
    FORCE_LOCAL_FALLBACKS: bool = os.getenv("FORCE_LOCAL_FALLBACKS", "true").lower() == "true"

settings = Settings()
