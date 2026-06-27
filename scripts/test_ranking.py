"""
TalentX – Test Ranking Script (CLI Demo)
Run this to see ranking in action with sample data.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def main():
    print("=" * 60)
    print("🏆 TALENTX RANKING ENGINE – CLI DEMO")
    print("=" * 60)

    from app.config import SAMPLE_JD_PATH, SAMPLE_RESUMES_DIR
    from app.ranking_engine import get_ranking_engine

    # Load sample JD
    with open(SAMPLE_JD_PATH, "r", encoding="utf-8") as f:
        jd_text = f.read()

    print(f"\n📄 JD: {jd_text[:200]}...\n")

    # Load sample resumes
    resumes = []
    for fname in sorted(os.listdir(SAMPLE_RESUMES_DIR)):
        if fname.endswith(".txt"):
            with open(SAMPLE_RESUMES_DIR / fname, "r", encoding="utf-8") as f:
                content = f.read()
            name = content.split("\n")[0].replace("RESUME –", "").strip()
            resumes.append({"name": name, "content": content})

    print(f"👥 Loaded {len(resumes)} candidate resumes\n")
    print("⚡ Ranking candidates...\n")

    engine = get_ranking_engine()
    result = engine.rank_candidates(jd_text, resumes)

    print(f"{'Rank':<6} {'Name':<22} {'Total':>7} {'Skill':>7} {'Semantic':>9} {'Exp':>6} {'Edu':>6}")
    print("-" * 65)

    for c in result.ranked_candidates:
        rank_str = f"{'🥇' if c.rank==1 else '🥈' if c.rank==2 else '🥉' if c.rank==3 else f'#{c.rank}'}"
        print(
            f"{rank_str:<6} {c.name:<22} {c.total_score:>6.1f}%"
            f" {c.skill_match:>6.0f}% {c.semantic_similarity:>8.0f}%"
            f" {c.experience_fit:>5.0f}% {c.education_fit:>5.0f}%"
        )

    print("\n" + "=" * 60)
    print(f"🏆 TOP PICK: {result.top_pick}")
    print("=" * 60)
    print(f"\n📊 {result.evaluation_note}\n")

    # Show top candidate details
    top = result.ranked_candidates[0]
    print(f"🔍 TOP CANDIDATE DETAILS: {top.name}")
    print(f"   Summary: {top.summary}")
    print(f"   ✅ Matched Skills: {', '.join(top.matched_skills[:8])}")
    if top.missing_skills:
        print(f"   ❌ Missing Skills: {', '.join(top.missing_skills[:5])}")
    print(f"   📚 Education: {top.education_level}")
    print(f"   ⏱️  Experience: {top.years_experience:.0f} years\n")


if __name__ == "__main__":
    main()
