"""
TalentX – Decision, Risk, and Family Engine Tests
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.decision_engine import DecisionEngine, _detect_options, _calculate_confidence
from app.risk_engine import RiskEngine, get_risk_engine
from app.family_engine import FamilyEngine, get_family_engine
from app.models import CandidateDecisionRequest, RiskRequest, FamilyDecisionRequest
from app.bharat_knowledge import BharatKnowledge


class TestDecisionEngine:

    @pytest.fixture
    def engine(self):
        return DecisionEngine()

    def test_option_detection_gate(self):
        query = "Should I prepare for GATE or go for placements?"
        options = _detect_options(query)
        assert "gate" in options

    def test_option_detection_startup(self):
        query = "I want to build a startup instead of taking a job"
        options = _detect_options(query)
        assert "startup" in options

    def test_option_detection_abroad(self):
        query = "I'm confused between MS abroad and placement in India"
        options = _detect_options(query)
        assert "abroad" in options

    def test_option_detection_fallback(self):
        # Even vague queries should return at least 2 options
        query = "I am confused about my career"
        options = _detect_options(query)
        assert len(options) >= 2

    def test_simulate_returns_options(self, engine):
        req = CandidateDecisionRequest(query="Should I do GATE or placement?")
        result = engine.simulate_options(req)
        assert len(result.options) >= 2

    def test_options_have_required_fields(self, engine):
        req = CandidateDecisionRequest(query="Should I do MBA or data science?")
        result = engine.simulate_options(req)
        for opt in result.options:
            assert opt.name
            assert opt.risk_level in ("Low", "Medium", "High")
            assert 0 <= opt.risk_score <= 100
            assert 0 <= opt.confidence <= 100
            assert isinstance(opt.pros, list)
            assert isinstance(opt.cons, list)
            assert isinstance(opt.timeline, list)

    def test_recommendation_generated(self, engine):
        req = CandidateDecisionRequest(query="GATE vs placement vs startup")
        result = engine.simulate_options(req)
        assert result.recommendation
        assert len(result.recommendation) > 20

    def test_bharat_context_with_location(self, engine):
        req = CandidateDecisionRequest(query="Career options after BTech", location="Odisha")
        result = engine.simulate_options(req)
        if result.bharat_context:
            assert "odisha" in result.bharat_context.lower() or "scholarship" in result.bharat_context.lower()


class TestRiskEngine:

    @pytest.fixture
    def engine(self):
        return RiskEngine()

    def test_high_risk_detected(self, engine):
        result = engine.assess_risk("I want to dropout and start a startup with no savings and no experience")
        # Financial risk should be high for this scenario
        financial = next(r for r in result.risks if "Financial" in r.risk_type)
        assert financial.level in ("Medium", "High"), f"Financial risk should be Medium/High, got: {financial.level}"
        # Overall should not be "Low" given high financial risk
        assert result.overall_risk in ("Medium", "High")
        # Overall score should be > 20 (not rock bottom)
        assert result.overall_score > 20

    def test_low_risk_option(self, engine):
        result = engine.assess_risk("I want to apply for campus placements at top companies")
        assert result.overall_risk in ("Low", "Medium")

    def test_four_risk_types(self, engine):
        result = engine.assess_risk("I want to dropout and startup", "2nd year, no savings")
        assert len(result.risks) == 4
        risk_types = {r.risk_type for r in result.risks}
        assert len(risk_types) == 4

    def test_alternatives_provided(self, engine):
        result = engine.assess_risk("I want to dropout")
        assert len(result.safer_alternatives) > 0

    def test_risk_scores_in_range(self, engine):
        result = engine.assess_risk("Going abroad for MS without savings")
        for risk in result.risks:
            assert 0 <= risk.score <= 100

    def test_singleton(self):
        e1 = get_risk_engine()
        e2 = get_risk_engine()
        assert e1 is e2


class TestFamilyEngine:

    @pytest.fixture
    def engine(self):
        return FamilyEngine()

    def test_balance_returns_response(self, engine):
        req = FamilyDecisionRequest(
            student_view="I want to go abroad for MS and pursue AI research",
            parent_view="We want stability and a good salary near home",
        )
        result = engine.balance_views(req)
        assert result.balanced_recommendation
        assert result.compromise_path
        assert 0 <= result.student_satisfaction <= 10
        assert 0 <= result.parent_satisfaction <= 10
        assert 0 <= result.compromise_score <= 100

    def test_action_steps_provided(self, engine):
        req = FamilyDecisionRequest(
            student_view="I want to start a startup",
            parent_view="We need income and stability"
        )
        result = engine.balance_views(req)
        assert len(result.action_steps) > 0

    def test_key_insight_generated(self, engine):
        req = FamilyDecisionRequest(
            student_view="I am passionate about research",
            parent_view="Income is more important than passion",
            student_name="Rahul"
        )
        result = engine.balance_views(req)
        assert result.key_insight
        assert "Rahul" in result.key_insight or "tension" in result.key_insight.lower()

    def test_singleton(self):
        e1 = get_family_engine()
        e2 = get_family_engine()
        assert e1 is e2


class TestBharatKnowledge:

    @pytest.fixture
    def knowledge(self):
        return BharatKnowledge()

    def test_scholarships_central(self, knowledge):
        result = knowledge.get_scholarships("all")
        assert result.total_found > 0
        assert len(result.central_schemes) > 0

    def test_scholarships_odisha(self, knowledge):
        result = knowledge.get_scholarships("odisha")
        assert result.state == "odisha"

    def test_career_outlook_ai(self, knowledge):
        result = knowledge.get_career_outlook("ai_ml_engineer")
        assert result.title
        assert result.avg_salary
        assert len(result.key_skills) > 0

    def test_career_outlook_generic(self, knowledge):
        result = knowledge.get_career_outlook("random_unknown_field")
        assert result.title  # Should not crash — returns generic

    def test_state_list(self, knowledge):
        states = knowledge.list_states()
        assert len(states) > 5
        assert "odisha" in states


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
