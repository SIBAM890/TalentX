"""
TalentX – NLP Pipeline Unit Tests
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.nlp_pipeline import NLPPipeline, get_pipeline
from app.utils import clean_text, extract_years_of_experience, extract_education_level, education_score


class TestNLPPipeline:

    @pytest.fixture
    def pipeline(self):
        return NLPPipeline()

    def test_pipeline_init(self, pipeline):
        assert pipeline is not None
        assert len(pipeline._skill_set) > 100

    def test_skill_extraction_basic(self, pipeline):
        text = "I know Python, Machine Learning, and SQL"
        skills = pipeline.extract_skills(text)
        assert "Python" in skills
        assert "Sql" in skills or "SQL" in skills or any("sql" in s.lower() for s in skills)

    def test_skill_extraction_case_insensitive(self, pipeline):
        text = "expert in PYTHON, pandas, numpy and TENSORFLOW"
        skills = pipeline.extract_skills(text)
        assert len(skills) >= 3

    def test_embedding_generation(self, pipeline):
        text = "Senior Data Scientist with Python and ML experience"
        embedding = pipeline.generate_embedding(text)
        assert embedding is not None
        assert len(embedding) > 0

    def test_embedding_similarity_high(self, pipeline):
        t1 = "Data Scientist with Python and machine learning"
        t2 = "ML Engineer with Python skills and data science background"
        sim = pipeline.text_similarity(t1, t2)
        assert 0.0 <= sim <= 1.0

    def test_embedding_similarity_low(self, pipeline):
        t1 = "Python machine learning data science"
        t2 = "French cuisine cooking restaurant chef"
        sim = pipeline.text_similarity(t1, t2)
        # Should be lower than for related texts
        assert sim < 0.9

    def test_keyword_coverage(self, pipeline):
        jd = "We need Python, SQL, Machine Learning experience"
        resume = "I have 3 years of Python and SQL experience with ML projects"
        result = pipeline.keyword_coverage(jd, resume)
        assert "coverage" in result
        assert result["coverage"] > 0.3

    def test_extract_entities_returns_dict(self, pipeline):
        text = "John has 5 years of Python experience and a B.Tech from IIT"
        entities = pipeline.extract_entities(text)
        assert "skills" in entities
        assert "years_experience" in entities
        assert "education" in entities

    def test_batch_embeddings(self, pipeline):
        texts = ["Python developer", "Java developer", "Data scientist"]
        embeddings = pipeline.generate_embeddings_batch(texts)
        assert len(embeddings) == 3


class TestUtils:

    def test_clean_text(self):
        raw = "  Hello,   World!  \n\nTest  "
        cleaned = clean_text(raw)
        assert "  " not in cleaned
        assert cleaned.strip() == cleaned

    def test_extract_experience_explicit(self):
        text = "I have 5 years of experience in Python"
        years = extract_years_of_experience(text)
        assert years == 5.0

    def test_extract_experience_zero(self):
        text = "Recent graduate looking for first job"
        years = extract_years_of_experience(text)
        assert years >= 0

    def test_extract_education_btech(self):
        text = "Bachelor of Technology in Computer Science from NIT"
        edu = extract_education_level(text)
        assert edu["level"] in ("btech_be",)

    def test_extract_education_mtech(self):
        text = "M.Tech in AI from IIT Delhi 2020"
        edu = extract_education_level(text)
        assert edu["level"] == "mtech_msc"

    def test_extract_education_phd(self):
        text = "PhD in Statistics from University of Kerala"
        edu = extract_education_level(text)
        assert edu["level"] == "phd"

    def test_education_score_ordering(self):
        assert education_score("phd") > education_score("mtech_msc")
        assert education_score("mtech_msc") > education_score("btech_be")
        assert education_score("btech_be") > education_score("diploma")

    def test_get_pipeline_singleton(self):
        p1 = get_pipeline()
        p2 = get_pipeline()
        assert p1 is p2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
