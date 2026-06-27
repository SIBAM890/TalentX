"""
TalentX – Recruiter Tab (TalentX Mode)
Intelligent candidate ranking with score breakdown.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.config import SAMPLE_JD_PATH, SAMPLE_RESUMES_DIR


def _direct_rank(jd_text: str, resumes: list[dict]):
    from app.ranking_engine import get_ranking_engine
    engine = get_ranking_engine()
    return engine.rank_candidates(jd_text, resumes)


def _load_sample_data():
    with open(SAMPLE_JD_PATH, "r", encoding="utf-8") as f:
        jd = f.read()
    resumes = []
    for fname in sorted(os.listdir(SAMPLE_RESUMES_DIR)):
        if fname.endswith(".txt"):
            with open(SAMPLE_RESUMES_DIR / fname, "r", encoding="utf-8") as f:
                content = f.read()
            name = content.split("\n")[0].replace("RESUME –", "").strip()
            resumes.append({"name": name, "content": content})
    return jd, resumes


def _score_color(score: float) -> str:
    if score >= 75:
        return "#43D9B3"
    elif score >= 55:
        return "#FFC107"
    else:
        return "#FF6584"


def _rank_emoji(rank: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")


def render_recruiter_tab():
    """Main render function for the Recruiter / TalentX tab."""

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255,101,132,0.12), rgba(108,99,255,0.08));
                border: 1px solid rgba(255,101,132,0.3); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;'>
        <h2 style='margin:0; color:#FF6584; font-family: Outfit, sans-serif;'>📊 TalentX Mode</h2>
        <p style='margin:0.3rem 0 0 0; color: #9999BB; font-size: 0.95rem;'>
        Intelligent candidate ranking. Beyond keywords — semantic understanding, skill match, experience fit.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Ranking Weights Display ─────────────────────────────────────────────────
    with st.expander("⚙️ Ranking Engine Weights"):
        w_cols = st.columns(5)
        weights = [("Skill Match", 35), ("Semantic", 25), ("Experience", 20), ("Education", 10), ("Keywords", 10)]
        for col, (label, pct) in zip(w_cols, weights):
            with col:
                st.markdown(f"**{label}**")
                st.progress(pct / 100)
                st.markdown(f"<center style='color:#6C63FF; font-weight:700;'>{pct}%</center>", unsafe_allow_html=True)

    # ── Mode Selection ─────────────────────────────────────────────────────────
    mode = st.radio(
        "Input Mode",
        ["📂 Load Sample Data (Demo)", "✍️ Enter Custom JD + Resumes"],
        horizontal=True,
        key="recruiter_mode"
    )

    jd_text = ""
    resumes = []

    if mode == "📂 Load Sample Data (Demo)":
        st.info("🚀 Will use the built-in sample Data Scientist JD and 10 sample resumes.")
        if st.button("🏃 Run Sample Ranking", key="sample_rank_btn", use_container_width=True):
            with st.spinner("⚡ Loading and ranking 10 candidates..."):
                try:
                    jd_text, resumes = _load_sample_data()
                    result = _direct_rank(jd_text, resumes)
                    st.session_state["ranking_result"] = result
                    st.session_state["ranking_jd"] = jd_text
                except Exception as e:
                    st.error(f"Ranking error: {e}")
    else:
        st.markdown("#### 📝 Job Description")
        jd_text = st.text_area(
            "Paste the full job description here",
            height=200,
            placeholder="We are looking for a Data Scientist with 3+ years of Python, ML, and NLP experience...",
            key="custom_jd"
        )

        st.markdown("#### 👥 Candidate Resumes")
        st.info("💡 Add at least 2 resumes. You can paste resume text directly.")

        num_resumes = st.slider("Number of resumes to input", 2, 8, 3, key="num_resumes")
        for i in range(num_resumes):
            with st.expander(f"Resume #{i+1}", expanded=(i < 2)):
                name_col, _ = st.columns([1, 2])
                with name_col:
                    rname = st.text_input(f"Candidate Name #{i+1}", key=f"rname_{i}", placeholder="e.g., Rahul Sharma")
                rcontent = st.text_area(f"Resume Text #{i+1}", key=f"rcontent_{i}", height=150,
                                        placeholder="Paste resume text here...")
                if rname and rcontent:
                    resumes.append({"name": rname, "content": rcontent})

        if st.button("🚀 Rank Candidates", key="custom_rank_btn", use_container_width=True):
            if not jd_text.strip():
                st.warning("Please enter a job description.")
            elif len(resumes) < 2:
                st.warning("Please add at least 2 complete resumes.")
            else:
                with st.spinner("⚡ Ranking candidates..."):
                    try:
                        result = _direct_rank(jd_text, resumes)
                        st.session_state["ranking_result"] = result
                        st.session_state["ranking_jd"] = jd_text
                    except Exception as e:
                        st.error(f"Ranking error: {e}")

    # ── Display Results ────────────────────────────────────────────────────────
    if "ranking_result" in st.session_state:
        _render_results(st.session_state["ranking_result"], st.session_state.get("ranking_jd", ""))


def _render_results(result, jd_text: str):
    st.markdown("---")
    st.markdown(f"### 🏆 Ranked Results — {result.total_candidates} Candidates")

    # ── Top 3 Podium ─────────────────────────────────────────────────────────
    if result.total_candidates >= 3:
        st.markdown("#### 🎖️ Top Picks")
        top3 = result.ranked_candidates[:3]
        p1, p2, p3 = st.columns(3)
        cols = [p2, p1, p3]  # 2nd, 1st, 3rd for podium feel
        rank_order = [1, 0, 2]
        podium_colors = ["#C0C0C0", "#FFD700", "#CD7F32"]
        for col, ridx, pcolor in zip(cols, rank_order, podium_colors):
            c = top3[ridx]
            with col:
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03); border: 2px solid {pcolor}40;
                            border-radius: 14px; padding: 1rem; text-align: center;'>
                    <div style='font-size: 2rem;'>{_rank_emoji(c.rank)}</div>
                    <div style='color: #F0F0FF; font-weight: 700; font-size: 1rem; margin: 0.3rem 0;'>{c.name}</div>
                    <div style='color: {pcolor}; font-size: 1.8rem; font-weight: 800;'>{c.total_score:.1f}</div>
                    <div style='color: #9999BB; font-size: 0.75rem;'>/ 100</div>
                    <div style='color: #9999BB; font-size: 0.78rem; margin-top: 0.4rem;'>{c.education_level} · {c.years_experience:.0f} yrs</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Full Ranked Table ─────────────────────────────────────────────────────
    st.markdown("#### 📋 Full Rankings")
    df = pd.DataFrame([
        {
            "Rank": _rank_emoji(c.rank),
            "Name": c.name,
            "Total Score": f"{c.total_score:.1f}",
            "Skill Match": f"{c.skill_match:.0f}%",
            "Semantic": f"{c.semantic_similarity:.0f}%",
            "Experience": f"{c.experience_fit:.0f}%",
            "Education": f"{c.education_fit:.0f}%",
            "Exp (yrs)": f"{c.years_experience:.0f}",
            "Education Level": c.education_level,
        }
        for c in result.ranked_candidates
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Export
    csv = df.to_csv(index=False)
    st.download_button(
        "⬇️ Export Rankings (CSV)",
        data=csv,
        file_name="talentx_rankings.csv",
        mime="text/csv",
        key="export_csv"
    )

    # ── Score Breakdown Radar Charts ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📡 Score Breakdown – Top 3 Candidates")
    if result.total_candidates > 0:
        _render_radar_charts(result.ranked_candidates[:min(3, result.total_candidates)])

    # ── Candidate Details ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🔍 Candidate Deep Dives")
    for candidate in result.ranked_candidates:
        color = _score_color(candidate.total_score)
        with st.expander(f"{_rank_emoji(candidate.rank)} **{candidate.name}** — {candidate.total_score:.1f}/100"):
            st.markdown(f"*{candidate.summary}*")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("**✅ Matched Skills:**")
                if candidate.matched_skills:
                    skills_html = " ".join([
                        f"<span style='background: rgba(67,217,179,0.15); border: 1px solid rgba(67,217,179,0.4); "
                        f"border-radius: 999px; padding: 2px 10px; font-size: 0.78rem; color: #43D9B3; margin: 2px; display: inline-block;'>{s}</span>"
                        for s in candidate.matched_skills[:10]
                    ])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.markdown("*None matched*")
            with c2:
                st.markdown("**❌ Missing Skills:**")
                if candidate.missing_skills:
                    miss_html = " ".join([
                        f"<span style='background: rgba(255,101,132,0.15); border: 1px solid rgba(255,101,132,0.4); "
                        f"border-radius: 999px; padding: 2px 10px; font-size: 0.78rem; color: #FF6584; margin: 2px; display: inline-block;'>{s}</span>"
                        for s in candidate.missing_skills[:8]
                    ])
                    st.markdown(miss_html, unsafe_allow_html=True)
                else:
                    st.markdown("*No critical gaps*")


def _render_radar_charts(candidates):
    """Render radar charts for top candidates."""
    dimensions = ["Skill Match", "Semantic", "Experience", "Education", "Keywords"]
    colors = ["#6C63FF", "#FF6584", "#43D9B3"]

    fig = go.Figure()
    for i, c in enumerate(candidates):
        values = [c.skill_match, c.semantic_similarity, c.experience_fit, c.education_fit, c.keyword_coverage]
        values.append(values[0])  # close the polygon
        theta = dimensions + [dimensions[0]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=theta,
            fill="toself",
            name=c.name,
            line_color=colors[i],
            fillcolor=colors[i].replace("FF", "33"),
            opacity=0.8,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#9999BB")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#9999BB")),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9999BB", family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        height=380,
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)
