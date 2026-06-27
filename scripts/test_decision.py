"""
TalentX – Test Decision Script (CLI Demo)
Run this to see DishaSetu Mode in action.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def demo_decision():
    from app.decision_engine import get_decision_engine
    from app.models import CandidateDecisionRequest

    engine = get_decision_engine()
    query = "I'm a BTech CSE student in Odisha confused between GATE, placements, and going abroad for MS"

    print(f"\n🎯 QUERY: {query}\n")
    req = CandidateDecisionRequest(query=query, user_background="3rd year BTech, CGPA 8.0", location="Odisha")
    result = engine.simulate_options(req)

    print(f"\n📊 OPTIONS COMPARISON ({len(result.options)} options identified)\n")
    print(f"{'Option':<30} {'Cost':>5} {'Risk':>7} {'Growth':>7} {'Confidence':>11}")
    print("-" * 65)
    for opt in result.options:
        print(f"{opt.name[:29]:<30} {opt.cost_score:>4.0f}% {opt.risk_score:>6.0f}% {opt.growth_score:>6.0f}% {opt.confidence:>10.0f}%")

    print(f"\n🏆 RECOMMENDATION:\n{result.recommendation}\n")

    if result.bharat_context:
        print(f"🇮🇳 BHARAT CONTEXT:\n{result.bharat_context}\n")

    # Show top option timeline
    top = result.options[0]
    print(f"📅 TIMELINE FOR: {top.name}")
    for m in top.timeline[:5]:
        print(f"   Year {m.year}: {m.milestone}")
        print(f"           → {m.action}")


def demo_risk():
    from app.risk_engine import get_risk_engine

    engine = get_risk_engine()
    option = "I want to drop out of college and build a startup with no savings and no experience"
    print(f"\n🛡️  RISK ASSESSMENT")
    print(f"   Option: {option[:70]}...\n")

    result = engine.assess_risk(option)
    print(f"   ⚠️  Overall Risk: {result.overall_risk} ({result.overall_score:.0f}/100)\n")

    for risk in result.risks:
        bar = "█" * int(risk.score // 10) + "░" * (10 - int(risk.score // 10))
        print(f"   [{bar}] {risk.risk_type}: {risk.level} ({risk.score:.0f}/100)")

    print(f"\n💡 SAFER ALTERNATIVES:")
    for alt in result.safer_alternatives[:2]:
        print(f"   • {alt}")


def demo_family():
    from app.family_engine import get_family_engine
    from app.models import FamilyDecisionRequest

    engine = get_family_engine()
    req = FamilyDecisionRequest(
        student_view="I want to pursue AI research and go abroad for MS at MIT",
        parent_view="We need stability and income. Go for a good job in India near home.",
        student_name="Rohan"
    )

    print(f"\n👨‍👩‍👧 FAMILY DECISION MODE")
    result = engine.balance_views(req)
    print(f"   🎓 Student Goal: {result.student_goal[:80]}...")
    print(f"   👨‍👩‍👧 Parent Concern: {result.parent_concern[:80]}...")
    print(f"\n   ⚖️  COMPROMISE: {result.balanced_recommendation}")
    print(f"   📊 Compromise Score: {result.compromise_score:.0f}%")
    print(f"   🎓 Student Satisfaction: {result.student_satisfaction}/10")
    print(f"   👨‍👩‍👧 Parent Satisfaction: {result.parent_satisfaction}/10")
    print(f"\n   💡 KEY INSIGHT: {result.key_insight}")
    print(f"\n   ✅ ACTION STEPS:")
    for i, step in enumerate(result.action_steps, 1):
        print(f"   {i}. {step}")


if __name__ == "__main__":
    print("=" * 65)
    print("🚀 TALENTX DECISION ENGINE – CLI DEMO")
    print("=" * 65)

    demo_decision()
    print("\n" + "=" * 65)
    demo_risk()
    print("\n" + "=" * 65)
    demo_family()
    print("\n" + "=" * 65 + "\n")
