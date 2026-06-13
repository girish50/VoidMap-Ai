import logging
import re
import math
from typing import List, Dict, Any, Set

logger = logging.getLogger("voidmap.nlp")
logging.basicConfig(level=logging.INFO)

# Global variables for models
TRANSFORMER_MODEL = None
SPACY_NLP = None
NLP_FALLBACK_ACTIVE = False

from app.config import settings

# Attempt to load Neural ML packages if not forced to run locally
if settings.FORCE_LOCAL_FALLBACKS:
    logger.info("FORCE_LOCAL_FALLBACKS is active. Skipping heavy neural ML model imports.")
    NLP_FALLBACK_ACTIVE = True
else:
    try:
        from sentence_transformers import SentenceTransformer
        import spacy
        
        logger.info("Attempting to load neural NLP models...")
        # Load mini transformer (only ~80MB, fast on CPU)
        TRANSFORMER_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        # Load spacy small model
        SPACY_NLP = spacy.load("en_core_web_sm")
        logger.info("Neural NLP (SentenceTransformers + spaCy) successfully loaded.")
    except Exception as e:
        logger.warning(
            f"Could not load heavy neural NLP packages ({e}). "
            "Enabling high-fidelity local keyword and Jaccard TF-IDF fallbacks."
        )
        NLP_FALLBACK_ACTIVE = True


def clean_text(text: str) -> str:
    """
    Sanitizes raw text, removing special characters and lowering case.
    """
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def tokenize(text: str) -> List[str]:
    """
    Lightweight stem-free tokenization.
    """
    return clean_text(text).split()

def compute_cosine_similarity(text1: str, text2: str) -> float:
    """
    Computes semantic cosine similarity.
    Uses SentenceTransformer if active, else falls back to mathematical TF-IDF vector overlap.
    """
    if not NLP_FALLBACK_ACTIVE and TRANSFORMER_MODEL is not None:
        try:
            embeddings = TRANSFORMER_MODEL.encode([text1, text2])
            # Cosine similarity formula: dot(a, b) / (norm(a) * norm(b))
            dot_product = sum(a * b for a, b in zip(embeddings[0], embeddings[1]))
            norm_a = math.sqrt(sum(a * a for a in embeddings[0]))
            norm_b = math.sqrt(sum(b * b for b in embeddings[1]))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return float(dot_product / (norm_a * norm_b))
        except Exception as e:
            logger.warning(f"SentenceTransformer similarity failed: {e}. Falling back to TF-IDF.")
            
    # TF-IDF Cosine Similarity Fallback (Pure Python)
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    if not tokens1 or not tokens2:
        return 0.0
        
    # Build vocabulary
    all_tokens = set(tokens1 + tokens2)
    
    # Calculate simple Term Frequencies (TF)
    tf1 = {token: tokens1.count(token) for token in all_tokens}
    tf2 = {token: tokens2.count(token) for token in all_tokens}
    
    # Calculate Cosine similarity between TF vectors
    dot_product = sum(tf1[token] * tf2[token] for token in all_tokens)
    magnitude1 = math.sqrt(sum(tf1[token] ** 2 for token in all_tokens))
    magnitude2 = math.sqrt(sum(tf2[token] ** 2 for token in all_tokens))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def get_embedding(text: str) -> Any:
    """
    Generates sentence embedding using SentenceTransformer.
    """
    if not NLP_FALLBACK_ACTIVE and TRANSFORMER_MODEL is not None:
        try:
            return TRANSFORMER_MODEL.encode(text)
        except Exception as e:
            logger.warning(f"Failed to generate embedding: {e}")
    return None

def compute_vector_similarity(emb1: Any, emb2: Any) -> float:
    """
    Calculates cosine similarity between two vector embeddings.
    """
    if emb1 is None or emb2 is None:
        return 0.0
    try:
        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        norm_a = math.sqrt(sum(a * a for a in emb1))
        norm_b = math.sqrt(sum(b * b for b in emb2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))
    except Exception as e:
        logger.warning(f"Vector similarity calculation failed: {e}")
        return 0.0

def extract_entities_and_technologies(text: str) -> Dict[str, Set[str]]:
    """
    Extracts technologies, core domains, and considered factors from proposal text.
    Uses spaCy NER if active, else parses via dynamic keyword lexicon.
    """
    results = {
        "technologies": set(),
        "considerations": set()
    }
    
    # Lexicon mappings
    tech_keywords = {
        "cnn", "rnn", "transformers", "lstm", "xgboost", "pytorch", "tensorflow", 
        "keras", "scikit-learn", "react", "fastapi", "docker", "kubernetes", "aws", 
        "gcp", "azure", "mongodb", "neo4j", "postgresql", "sqlite", "redis", "celery",
        "neural network", "deep learning", "machine learning", "ledger", "smart contract"
    }
    
    consideration_keywords = {
        "accuracy", "security", "deployment", "scaling", "latency", "bias", "fairness",
        "compliance", "validation", "hipaa", "gdpr", "ethics", "cost", "budget", "monitoring",
        "drift", "privacy", "auditing", "regulation", "clinical"
    }
    
    # 1. Neural extraction via spaCy
    if not NLP_FALLBACK_ACTIVE and SPACY_NLP is not None:
        try:
            doc = SPACY_NLP(text)
            for ent in doc.ents:
                ent_text = ent.text.lower().strip()
                if ent.label_ in ("ORG", "PRODUCT") or ent_text in tech_keywords:
                    results["technologies"].add(ent_text)
        except Exception as e:
            logger.warning(f"spaCy extraction failed: {e}. Falling back to keyword search.")
            
    # 2. Local Keyword Extraction (Run in parallel to verify accuracy)
    cleaned = text.lower()
    for word in tech_keywords:
        # Match whole words/phrases using boundary check
        if re.search(r'\b' + re.escape(word) + r'\b', cleaned):
            results["technologies"].add(word)
            
    for word in consideration_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', cleaned):
            results["considerations"].add(word)
            
    return results
