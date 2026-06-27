"""
TalentX – Hybrid Ranking Engine
Weights: skill_match(35%) + semantic(25%) + experience(20%) + education(10%) + keywords(10%)
"""
import logging
from app.config import RANKING_WEIGHTS
from app.utils import clamp, education_score, extract_years_of_experience, extract_education_level
from app.nlp_pipeline import get_pipeline
from app.models import CandidateScore, RecruiterRankResponse

logger = logging.getLogger("talentx.ranking")


def _compute_skill_match(jd_skills: list[str], resume_skills: list[str]) -> tuple[float, list[str], list[str]]:
    """Compute skill match score and return matched/missing skills."""
    if not jd_skills:
        return 50.0, [], []
    jd_lower = {s.lower() for s in jd_skills}
    resume_lower = {s.lower() for s in resume_skills}
    matched = [s for s in jd_skills if s.lower() in resume_lower]
    missing = [s for s in jd_skills if s.lower() not in resume_lower]
    score = (len(matched) / len(jd_skills)) * 100.0
    return round(score, 2), matched, missing


def _compute_experience_fit(jd_text: str, resume_text: str) -> float:
    """Score experience fit based on required vs actual years."""
    import re
    # Extract required years from JD
    req_match = re.search(r"(\d+)\+?\s*years?\s+(?:of\s+)?experience", jd_text.lower())
    required_years = float(req_match.group(1)) if req_match else 2.0

    actual_years = extract_years_of_experience(resume_text)

    if actual_years >= required_years * 1.5:
        return 100.0  # Overqualified but still good
    elif actual_years >= required_years:
        return 90.0 + (actual_years - required_years) * 2
    elif actual_years >= required_years * 0.7:
        return 70.0 + (actual_years / required_years) * 20
    elif actual_years > 0:
        return 40.0 + (actual_years / required_years) * 30
    else:
        return 20.0  # Fresher


def _generate_summary(name: str, score: float, matched: list[str], missing: list[str], years: float) -> str:
    """Generate a human-readable summary for a candidate."""
    if score >= 85:
        fit = "Excellent fit"
    elif score >= 70:
        fit = "Strong candidate"
    elif score >= 55:
        fit = "Moderate fit"
    else:
        fit = "Below threshold"

    skill_note = f"Matches {len(matched)} key skills." if matched else "Limited skill overlap."
    gap_note = f" Missing: {', '.join(missing[:3])}." if missing else ""
    exp_note = f" {years:.0f} years experience." if years > 0 else " Fresher profile."

    return f"{fit}. {skill_note}{gap_note}{exp_note}"


class RankingEngine:
    """Hybrid multi-dimensional candidate ranking engine."""

    def __init__(self):
        self.weights = RANKING_WEIGHTS
        self.pipeline = get_pipeline()

    def rank_candidates(
        self,
        jd_text: str,
        resumes: list[dict],  # [{"name": str, "content": str}, ...]
    ) -> RecruiterRankResponse:
        """
        Rank candidates against a job description.
        Returns fully structured RecruiterRankResponse.
        """
        logger.info(f"Ranking {len(resumes)} candidates against JD")

        # Extract JD entities
        jd_entities = self.pipeline.extract_entities(jd_text)
        jd_skills = jd_entities["skills"]
        jd_embedding = self.pipeline.generate_embedding(jd_text)

        # Generate all resume embeddings in batch
        resume_texts = [r["content"] for r in resumes]
        resume_embeddings = self.pipeline.generate_embeddings_batch(resume_texts)

        scored = []
        for i, resume in enumerate(resumes):
            name = resume["name"]
            content = resume["content"]
            embedding = resume_embeddings[i]

            # 1. Skill match
            resume_entities = self.pipeline.extract_entities(content)
            resume_skills = resume_entities["skills"]
            skill_score, matched, missing = _compute_skill_match(jd_skills, resume_skills)

            # 2. Semantic similarity
            raw_sim = self.pipeline.compute_similarity(jd_embedding, embedding)
            semantic_score = clamp(raw_sim * 100, 0, 100)

            # 3. Experience fit
            exp_score = _compute_experience_fit(jd_text, content)
            years_exp = resume_entities["years_experience"]

            # 4. Education fit
            edu = resume_entities["education"]
            edu_score = education_score(edu["level"])

            # 5. Keyword coverage
            kw = self.pipeline.keyword_coverage(jd_text, content)
            kw_score = clamp(kw["coverage"] * 100, 0, 100)

            # Weighted total
            total = (
                self.weights["skill_match"] * skill_score
                + self.weights["semantic_similarity"] * semantic_score
                + self.weights["experience_fit"] * exp_score
                + self.weights["education_fit"] * edu_score
                + self.weights["keyword_coverage"] * kw_score
            )

            summary = _generate_summary(name, total, matched, missing, years_exp)

            scored.append(CandidateScore(
                name=name,
                rank=0,  # assigned below
                total_score=round(total, 2),
                skill_match=round(skill_score, 2),
                semantic_similarity=round(semantic_score, 2),
                experience_fit=round(exp_score, 2),
                education_fit=round(edu_score, 2),
                keyword_coverage=round(kw_score, 2),
                years_experience=years_exp,
                education_level=edu["display"],
                matched_skills=matched[:10],
                missing_skills=missing[:8],
                summary=summary,
            ))

        # Sort and assign ranks
        scored.sort(key=lambda c: c.total_score, reverse=True)
        for rank, candidate in enumerate(scored, start=1):
            candidate.rank = rank

        jd_summary = jd_text[:200].replace("\n", " ").strip() + "..."
        top_pick = scored[0].name if scored else "N/A"

        return RecruiterRankResponse(
            jd_summary=jd_summary,
            total_candidates=len(scored),
            ranked_candidates=scored,
            top_pick=top_pick,
            evaluation_note=(
                f"Evaluated {len(scored)} candidates. "
                f"Weights: Skill {int(self.weights['skill_match']*100)}%, "
                f"Semantic {int(self.weights['semantic_similarity']*100)}%, "
                f"Experience {int(self.weights['experience_fit']*100)}%, "
                f"Education {int(self.weights['education_fit']*100)}%, "
                f"Keywords {int(self.weights['keyword_coverage']*100)}%."
            ),
        )


# Singleton
_ranking_instance = None


def get_ranking_engine() -> RankingEngine:
    global _ranking_instance
    if _ranking_instance is None:
        _ranking_instance = RankingEngine()
    return _ranking_instance
