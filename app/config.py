"""
TalentX – Configuration Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_RESUMES_DIR = DATA_DIR / "sample_resumes"

# App settings
APP_ENV = os.getenv("APP_ENV", "development")
APP_DEBUG = os.getenv("APP_DEBUG", "true").lower() == "true"
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Model settings
SENTENCE_BERT_MODEL = os.getenv("SENTENCE_BERT_MODEL", "all-MiniLM-L6-v2")
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
USE_GPU = os.getenv("USE_GPU", "false").lower() == "true"

# OpenRouter / LLM settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_VERIFY_SSL = os.getenv("OPENROUTER_VERIFY_SSL", "true").lower() == "true"
LLM_ENABLED = os.getenv("LLM_ENABLED", "true").lower() == "true"

# Frontend
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Ranking engine weights
RANKING_WEIGHTS = {
    "skill_match": 0.35,
    "semantic_similarity": 0.25,
    "experience_fit": 0.20,
    "education_fit": 0.10,
    "keyword_coverage": 0.10,
}

# Risk thresholds
RISK_LEVELS = {
    "low": (0, 33),
    "medium": (34, 66),
    "high": (67, 100),
}

# Data file paths
SKILL_TAXONOMY_PATH = DATA_DIR / "skill_taxonomy.json"
CAREER_PATHS_PATH = DATA_DIR / "career_paths.json"
SCHOLARSHIP_DATA_PATH = DATA_DIR / "scholarship_data.json"
SAMPLE_JD_PATH = DATA_DIR / "sample_jd.txt"
