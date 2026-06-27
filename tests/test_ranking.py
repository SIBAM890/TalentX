"""
TalentX – Ranking Engine Unit Tests
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.ranking_engine import RankingEngine, get_ranking_engine, _compute_skill_match, _compute_experience_fit


SAMPLE_JD = """
We are looking for a Data Scientist with 3+ years of experience.
Required: Python, Machine Learning, SQL, Deep Learning, TensorFlow.
Experience with AWS SageMaker preferred.
B.Tech or M.Tech in CS required.
"""

RESUME_STRONG = """
RESUME - Rahul Sharma
Senior Data Scientist with 5 years of experience.
Skills: Python, Machine Learning, Deep Learning, TensorFlow, SQL, AWS
M.Tech in Computer Science from IIT Bombay.
Built ML models at Razorpay serving 10M users.
"""

RESUME_WEAK = """
RESUME - Ananya Das
Data Analyst, 2 years experience.
Skills: Excel, Power BI, Tableau, Google Analytics
B.Sc Statistics.
Analyzed marketing data for EdTech startup.
"""

RESUME_MEDIUM = """
RESUME - Priya Mehta
Data Scientist, 3 years experience.
Skills: Python, Machine Learning, Scikit-learn, SQL, Pandas
B.Tech in Information Technology.
Built customer churn prediction model with XGBoost.
"""


class TestSkillMatch:

    def test_perfect_skill_match(self):
        jd_skills = ["Python", "Machine Learning", "SQL"]
        resume_skills = ["Python", "Machine Learning", "SQL", "Pandas"]
        score, matched, missing = _compute_skill_match(jd_skills, resume_skills)
        assert score == 100.0
        assert len(matched) == 3
        assert len(missing) == 0

    def test_partial_skill_match(self):
        jd_skills = ["Python", "Machine Learning", "SQL", "Kubernetes"]
        resume_skills = ["Python", "Machine Learning"]
        score, matched, missing = _compute_skill_match(jd_skills, resume_skills)
        assert score == 50.0
        assert "Kubernetes" in missing

    def test_zero_skill_match(self):
        jd_skills = ["Python", "Machine Learning"]
        resume_skills = ["Excel", "PowerPoint"]
        score, matched, missing = _compute_skill_match(jd_skills, resume_skills)
        assert score == 0.0

    def test_empty_jd_skills(self):
        score, matched, missing = _compute_skill_match([], ["Python"])
        assert score == 50.0  # Default when no JD skills


class TestExperienceFit:

    def test_exact_experience_match(self):
        jd = "We need 3 years of experience"
        resume = "Senior developer with 3 years of experience"
        score = _compute_experience_fit(jd, resume)
        assert score >= 80.0

    def test_overqualified(self):
        jd = "We need 2 years of experience"
        resume = "Professional with 8 years of experience"
        score = _compute_experience_fit(jd, resume)
        assert score >= 85.0

    def test_underqualified(self):
        jd = "We need 5 years of experience"
        resume = "Fresher with no experience"
        score = _compute_experience_fit(jd, resume)
        assert score < 50.0


class TestRankingEngine:

    @pytest.fixture
    def engine(self):
        return RankingEngine()

    def test_ranking_produces_results(self, engine):
        resumes = [
            {"name": "Strong", "content": RESUME_STRONG},
            {"name": "Weak", "content": RESUME_WEAK},
        ]
        result = engine.rank_candidates(SAMPLE_JD, resumes)
        assert result.total_candidates == 2
        assert len(result.ranked_candidates) == 2

    def test_ranking_is_ordered(self, engine):
        resumes = [
            {"name": "Strong", "content": RESUME_STRONG},
            {"name": "Weak", "content": RESUME_WEAK},
        ]
        result = engine.rank_candidates(SAMPLE_JD, resumes)
        scores = [c.total_score for c in result.ranked_candidates]
        assert scores == sorted(scores, reverse=True)

    def test_strong_beats_weak(self, engine):
        resumes = [
            {"name": "Strong", "content": RESUME_STRONG},
            {"name": "Weak", "content": RESUME_WEAK},
        ]
        result = engine.rank_candidates(SAMPLE_JD, resumes)
        ranked_names = [c.name for c in result.ranked_candidates]
        assert ranked_names.index("Strong") < ranked_names.index("Weak")

    def test_scores_in_valid_range(self, engine):
        resumes = [
            {"name": "Medium", "content": RESUME_MEDIUM},
        ]
        result = engine.rank_candidates(SAMPLE_JD, resumes)
        for c in result.ranked_candidates:
            assert 0 <= c.total_score <= 100
            assert 0 <= c.skill_match <= 100
            assert 0 <= c.semantic_similarity <= 100

    def test_candidate_has_required_fields(self, engine):
        resumes = [{"name": "Test", "content": RESUME_MEDIUM}]
        result = engine.rank_candidates(SAMPLE_JD, resumes)
        c = result.ranked_candidates[0]
        assert c.name == "Test"
        assert c.rank == 1
        assert c.summary is not None
        assert isinstance(c.matched_skills, list)

    def test_singleton_engine(self):
        e1 = get_ranking_engine()
        e2 = get_ranking_engine()
        assert e1 is e2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
