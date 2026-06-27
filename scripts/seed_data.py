"""
TalentX – Sample Data Seed Script
Validates all data files and shows statistics.
"""
import sys, os, json
# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import SKILL_TAXONOMY_PATH, CAREER_PATHS_PATH, SCHOLARSHIP_DATA_PATH, SAMPLE_RESUMES_DIR
from app.utils import load_json


def validate_skill_taxonomy():
    print("\n📚 SKILL TAXONOMY")
    print("=" * 50)
    data = load_json(SKILL_TAXONOMY_PATH)
    total = 0
    for category, info in data.items():
        skills = info.get("skills", [])
        total += len(skills)
        print(f"  ✅ {info.get('category', category)}: {len(skills)} skills")
    print(f"  TOTAL: {total} skills")
    return total


def validate_career_paths():
    print("\n🛤️  CAREER PATHS")
    print("=" * 50)
    data = load_json(CAREER_PATHS_PATH)
    for key, path in data.items():
        milestones = len(path.get("yearly_milestones", []))
        skills = len(path.get("skills_required", []))
        print(f"  ✅ {path.get('title', key)}: {milestones} milestones, {skills} skills, salary: {path.get('avg_salary', 'N/A')}")
    print(f"  TOTAL: {len(data)} career paths")
    return len(data)


def validate_scholarships():
    print("\n🎓 SCHOLARSHIP DATA")
    print("=" * 50)
    data = load_json(SCHOLARSHIP_DATA_PATH)
    central = len(data.get("central_schemes", []))
    states = data.get("state_schemes", {})
    private = len(data.get("private_scholarships", []))
    state_total = sum(len(v) for v in states.values())

    print(f"  ✅ Central Schemes: {central}")
    print(f"  ✅ State Coverage: {len(states)} states, {state_total} scholarships")
    for state, schemes in states.items():
        print(f"     → {state}: {len(schemes)} scholarships")
    print(f"  ✅ Private Scholarships: {private}")
    total = central + state_total + private
    print(f"  TOTAL: {total} scholarships")
    return total


def validate_resumes():
    print("\n📄 SAMPLE RESUMES")
    print("=" * 50)
    if not SAMPLE_RESUMES_DIR.exists():
        print("  ❌ Sample resumes directory not found")
        return 0
    resumes = list(SAMPLE_RESUMES_DIR.glob("*.txt"))
    for r in sorted(resumes):
        lines = r.read_text(encoding="utf-8").split("\n")
        name = lines[0].replace("RESUME –", "").strip() if lines else r.stem
        print(f"  ✅ {name} ({r.stat().st_size // 1024 + 1}KB)")
    print(f"  TOTAL: {len(resumes)} sample resumes")
    return len(resumes)


def run_quick_smoke_test():
    print("\n🔥 SMOKE TESTS")
    print("=" * 50)

    # NLP Pipeline
    try:
        from app.nlp_pipeline import NLPPipeline
        p = NLPPipeline()
        skills = p.extract_skills("Python, Machine Learning, SQL, Docker")
        print(f"  ✅ NLP Pipeline: Extracted {len(skills)} skills from test text")
    except Exception as e:
        print(f"  ❌ NLP Pipeline: {e}")

    # Decision Engine
    try:
        from app.decision_engine import DecisionEngine
        from app.models import CandidateDecisionRequest
        engine = DecisionEngine()
        req = CandidateDecisionRequest(query="Should I do GATE or placement?")
        result = engine.simulate_options(req)
        print(f"  ✅ Decision Engine: Generated {len(result.options)} options")
    except Exception as e:
        print(f"  ❌ Decision Engine: {e}")

    # Ranking Engine
    try:
        from app.ranking_engine import RankingEngine
        engine = RankingEngine()
        jd = "Python ML engineer with 3 years experience"
        resumes = [
            {"name": "Alice", "content": "5 years Python Machine Learning TensorFlow ML engineer"},
            {"name": "Bob", "content": "Junior developer HTML CSS JavaScript"},
        ]
        result = engine.rank_candidates(jd, resumes)
        top = result.ranked_candidates[0].name
        print(f"  ✅ Ranking Engine: Ranked 2 candidates. Top: {top} ✓")
        assert top == "Alice", f"Expected Alice to rank first but got {top}"
    except Exception as e:
        print(f"  ❌ Ranking Engine: {e}")

    # Risk Engine
    try:
        from app.risk_engine import RiskEngine
        engine = RiskEngine()
        result = engine.assess_risk("I want to dropout and start a startup")
        print(f"  ✅ Risk Engine: {len(result.risks)} risks detected, overall: {result.overall_risk}")
    except Exception as e:
        print(f"  ❌ Risk Engine: {e}")

    # Family Engine
    try:
        from app.family_engine import FamilyEngine
        from app.models import FamilyDecisionRequest
        engine = FamilyEngine()
        req = FamilyDecisionRequest(student_view="I want to go abroad", parent_view="Stay in India and get a job")
        result = engine.balance_views(req)
        print(f"  ✅ Family Engine: Compromise score {result.compromise_score:.1f}%")
    except Exception as e:
        print(f"  ❌ Family Engine: {e}")

    # Bharat Knowledge
    try:
        from app.bharat_knowledge import BharatKnowledge
        knowledge = BharatKnowledge()
        result = knowledge.get_scholarships("odisha")
        print(f"  ✅ Bharat Knowledge: {result.total_found} scholarships for Odisha")
    except Exception as e:
        print(f"  ❌ Bharat Knowledge: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 TALENTX – DATA SEED VALIDATION")
    print("=" * 50)

    skills_count = validate_skill_taxonomy()
    paths_count = validate_career_paths()
    scholarship_count = validate_scholarships()
    resume_count = validate_resumes()
    run_quick_smoke_test()

    print("\n" + "=" * 50)
    print("✅ SUMMARY")
    print("=" * 50)
    print(f"  Skills:      {skills_count}")
    print(f"  Career Paths:{paths_count}")
    print(f"  Scholarships:{scholarship_count}")
    print(f"  Resumes:     {resume_count}")
    print("\n🎉 TalentX data validation complete! Ready to run.\n")
