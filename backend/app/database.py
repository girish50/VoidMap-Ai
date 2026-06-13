import logging
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings, BASE_DIR

logger = logging.getLogger("voidmap.database")

# Configure SQLite threading rules if DATABASE_URL starts with sqlite
def get_connect_args(url: str):
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}

db_url = settings.DATABASE_URL
engine = create_engine(
    db_url, 
    echo=False, 
    connect_args=get_connect_args(db_url)
)

def create_db_and_tables():
    """
    Initialize relational schemas and tables. Safe to call multiple times.
    If the primary database fails to connect, automatically fall back to local SQLite.
    """
    global engine, db_url
    from app.models import User, Project, Analysis, ExpertReview
    
    try:
        # Test connection validity
        with engine.connect() as conn:
            pass
        SQLModel.metadata.create_all(engine)
        logger.info(f"Database successfully connected & initialized at: {db_url}")
    except Exception as e:
        logger.error(f"Failed to connect to primary database at {db_url}. Error: {e}")
        if not db_url.startswith("sqlite"):
            sqlite_path = BASE_DIR / "voidmap.db"
            fallback_url = f"sqlite:///{sqlite_path}"
            logger.warning(f"DATABASE FALLBACK ACTIVATED: Switching to local SQLite at {fallback_url}")
            db_url = fallback_url
            engine = create_engine(
                db_url, 
                echo=False, 
                connect_args=get_connect_args(db_url)
            )
            SQLModel.metadata.create_all(engine)
            logger.info("Fallback SQLite database initialized successfully.")
        else:
            raise e

def get_session():
    """
    FastAPI Session Dependency. Automatically handles commits/rollbacks and session closing.
    """
    with Session(engine) as session:
        yield session

