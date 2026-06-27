"""
TalentX – Utility Functions
"""
import re
import json
import logging
import unicodedata
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("talentx")


def clean_text(text: str) -> str:
    """Normalize and clean text for NLP processing."""
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)
    # Remove special characters but keep punctuation
    text = re.sub(r"[^\w\s.,;:()\-+/]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Normalize a score to 0–100 range."""
    if max_val == min_val:
        return 0.0
    normalized = (score - min_val) / (max_val - min_val)
    return round(max(0.0, min(100.0, normalized * 100)), 2)


def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def load_json(path: Path) -> Any:
    """Load JSON data from file with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found: {path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in {path}: {e}")
        return {}


def extract_years_of_experience(text: str) -> float:
    """Extract total years of experience from resume text."""
    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"(\d+)\+?\s*years?\s+experience",
        r"experience\s+of\s+(\d+)\+?\s*years?",
        r"(\d+)\+?\s*yrs?\s+experience",
    ]
    max_years = 0.0
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            try:
                years = float(match)
                max_years = max(max_years, years)
            except ValueError:
                pass

    # Fallback: count date ranges (e.g., 2019 – 2022 = 3 years)
    if max_years == 0:
        date_ranges = re.findall(r"(20\d\d)\s*[–\-–]\s*(20\d\d|Present)", text, re.IGNORECASE)
        import datetime
        current_year = datetime.datetime.now().year
        for start, end in date_ranges:
            end_year = current_year if end.lower() == "present" else int(end)
            max_years += max(0, end_year - int(start))

    return min(max_years, 30.0)  # Cap at 30 years


def extract_education_level(text: str) -> dict:
    """Detect highest education level from text."""
    text_lower = text.lower()
    levels = {
        "phd": ["ph.d", "phd", "doctorate", "doctoral"],
        "mtech_msc": ["m.tech", "mtech", "m.sc", "msc", "master", "ms in", "m.e", "mba", "m.b.a"],
        "btech_be": ["b.tech", "btech", "b.e", "be in", "b.sc", "bsc", "bachelor", "b.com", "bca"],
        "diploma": ["diploma", "polytechnic"],
        "high_school": ["12th", "higher secondary", "class 12", "plus two", "intermediate"],
    }
    order = ["phd", "mtech_msc", "btech_be", "diploma", "high_school"]
    for level in order:
        for keyword in levels[level]:
            if keyword in text_lower:
                return {"level": level, "display": level.replace("_", "/").upper()}
    return {"level": "unknown", "display": "Not Specified"}


def education_score(level: str) -> float:
    """Score education level for ranking (0–100)."""
    scores = {
        "phd": 100,
        "mtech_msc": 85,
        "btech_be": 70,
        "diploma": 50,
        "high_school": 30,
        "unknown": 40,
    }
    return scores.get(level, 40)


def get_risk_label(score: float) -> str:
    """Convert numeric risk score to label."""
    if score <= 25:
        return "Low"
    elif score <= 60:
        return "Medium"
    else:
        return "High"


def get_risk_color(label: str) -> str:
    """Return color for risk label."""
    return {"Low": "green", "Medium": "orange", "High": "red"}.get(label, "gray")
