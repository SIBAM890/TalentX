"""
TalentX – NLP Pipeline
Sentence-BERT embeddings + spaCy NER + TF-IDF fallback
"""
import re
import logging
from typing import Optional
from app.config import SENTENCE_BERT_MODEL, SPACY_MODEL, SKILL_TAXONOMY_PATH
from app.utils import clean_text, load_json

logger = logging.getLogger("talentx.nlp")

# ─── Lazy-load heavy models ───────────────────────────────────────────────────
_sbert_model = None
_spacy_nlp = None
_tfidf_vectorizer = None
_skill_set: set[str] = set()


def _load_skill_set() -> set[str]:
    global _skill_set
    if _skill_set:
        return _skill_set
    taxonomy = load_json(SKILL_TAXONOMY_PATH)
    for category_data in taxonomy.values():
        for skill in category_data.get("skills", []):
            _skill_set.add(skill.lower())
    logger.info(f"Loaded {len(_skill_set)} skills into taxonomy")
    return _skill_set


def _get_sbert():
    """Load Sentence-BERT model (lazy, with fallback)."""
    global _sbert_model
    if _sbert_model is not None:
        return _sbert_model
    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading Sentence-BERT model: {SENTENCE_BERT_MODEL}")
        _sbert_model = SentenceTransformer(SENTENCE_BERT_MODEL)
        logger.info("Sentence-BERT model loaded successfully")
        return _sbert_model
    except Exception as e:
        logger.warning(f"Sentence-BERT not available ({e}). Falling back to TF-IDF.")
        return None


def _get_spacy():
    """Load spaCy model (lazy, with fallback)."""
    global _spacy_nlp
    if _spacy_nlp is not None:
        return _spacy_nlp
    try:
        import spacy
        _spacy_nlp = spacy.load(SPACY_MODEL)
        logger.info("spaCy model loaded successfully")
        return _spacy_nlp
    except Exception as e:
        logger.warning(f"spaCy not available ({e}). NER will use regex fallback.")
        return None


def _get_tfidf():
    """Get or create TF-IDF vectorizer for fallback similarity."""
    global _tfidf_vectorizer
    if _tfidf_vectorizer is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        _tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=5000,
        )
    return _tfidf_vectorizer


class NLPPipeline:
    """Core NLP pipeline for TalentX — embeddings, entity extraction, similarity."""

    def __init__(self):
        self._skill_set = _load_skill_set()

    # ─── ENTITY EXTRACTION ────────────────────────────────────────────────────

    def extract_skills(self, text: str) -> list[str]:
        """Extract skills from text using taxonomy matching."""
        text_lower = text.lower()
        found = []
        for skill in self._skill_set:
            # Word boundary match — avoid partial matches
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found.append(skill.title())
        return sorted(set(found))

    def extract_entities(self, text: str) -> dict:
        """Extract structured entities from resume/JD text."""
        cleaned = clean_text(text)
        skills = self.extract_skills(cleaned)

        # Try spaCy first
        nlp = _get_spacy()
        orgs, locations = [], []
        if nlp:
            doc = nlp(cleaned[:50000])  # spaCy limit
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    orgs.append(ent.text)
                elif ent.label_ in ("GPE", "LOC"):
                    locations.append(ent.text)

        from app.utils import extract_years_of_experience, extract_education_level
        years_exp = extract_years_of_experience(text)
        education = extract_education_level(text)

        return {
            "skills": skills,
            "organizations": list(set(orgs))[:10],
            "locations": list(set(locations))[:5],
            "years_experience": years_exp,
            "education": education,
        }

    # ─── EMBEDDINGS ───────────────────────────────────────────────────────────

    def generate_embedding(self, text: str):
        """Generate a vector embedding for text (SBERT or TF-IDF)."""
        cleaned = clean_text(text)[:10000]
        model = _get_sbert()
        if model is not None:
            return model.encode(cleaned, convert_to_numpy=True)
        # TF-IDF fallback
        vectorizer = _get_tfidf()
        try:
            return vectorizer.transform([cleaned]).toarray()[0]
        except Exception:
            vectorizer.fit([cleaned])
            return vectorizer.transform([cleaned]).toarray()[0]

    def generate_embeddings_batch(self, texts: list[str]):
        """Generate embeddings for a list of texts efficiently."""
        cleaned = [clean_text(t)[:10000] for t in texts]
        model = _get_sbert()
        if model is not None:
            return model.encode(cleaned, convert_to_numpy=True, batch_size=16, show_progress_bar=False)
        # TF-IDF fallback
        vectorizer = _get_tfidf()
        try:
            return vectorizer.transform(cleaned).toarray()
        except Exception:
            vectorizer.fit(cleaned)
            return vectorizer.transform(cleaned).toarray()

    # ─── SIMILARITY ───────────────────────────────────────────────────────────

    def compute_similarity(self, embedding1, embedding2) -> float:
        """Cosine similarity between two embeddings — returns 0 to 1."""
        import numpy as np
        e1 = np.array(embedding1).flatten()
        e2 = np.array(embedding2).flatten()
        norm1 = np.linalg.norm(e1)
        norm2 = np.linalg.norm(e2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(e1, e2) / (norm1 * norm2))

    def text_similarity(self, text1: str, text2: str) -> float:
        """End-to-end text similarity (0 to 1)."""
        e1 = self.generate_embedding(text1)
        e2 = self.generate_embedding(text2)
        return self.compute_similarity(e1, e2)

    # ─── KEYWORD MATCHING ─────────────────────────────────────────────────────

    def keyword_coverage(self, jd_text: str, resume_text: str) -> dict:
        """Compute keyword overlap between JD and resume."""
        def tokenize(t):
            return set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#\.]*\b", t.lower()))

        jd_tokens = tokenize(jd_text)
        resume_tokens = tokenize(resume_text)

        # Filter to meaningful words (length > 2, not stop words)
        stop = {"the", "and", "for", "with", "our", "you", "are", "this",
                "that", "have", "has", "will", "from", "can", "not", "all"}
        jd_keywords = {t for t in jd_tokens if len(t) > 2 and t not in stop}
        matched = jd_keywords & resume_tokens
        coverage = len(matched) / len(jd_keywords) if jd_keywords else 0.0

        return {
            "coverage": coverage,
            "matched_count": len(matched),
            "total_jd_keywords": len(jd_keywords),
            "matched_keywords": list(matched)[:20],
        }


# Singleton instance
_pipeline_instance: Optional[NLPPipeline] = None


def get_pipeline() -> NLPPipeline:
    """Return the singleton NLP pipeline instance."""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = NLPPipeline()
    return _pipeline_instance
