"""Recruiter mode UI for TalentX."""
import os
import sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.config import SAMPLE_JD_PATH, SAMPLE_RESUMES_DIR


def _direct_rank(jd_text: str, resumes: list[dict]):
    from app.ranking_engine import get_ranking_engine

    return get_ranking_engine().rank_candidates(jd_text, resumes)


def _load_sample_data():
    with open(SAMPLE_JD_PATH, "r", encoding="utf-8") as f:
        jd = f.read()

    resumes = []
    for filename in sorted(os.listdir(SAMPLE_RESUMES_DIR)):
        if filename.endswith(".txt"):
            with open(SAMPLE_RESUMES_DIR / filename, "r", encoding="utf-8") as f:
                content = f.read()
            name = content.split("\n")[0].replace("RESUME -", "").replace("RESUME –", "").strip()
            resumes.append({"name": name, "content": content})
    return jd, resumes


def _rank_label(rank: int) -> str:
    return {1: "1", 2: "2", 3: "3"}.get(rank, str(rank))


def render_recruiter_tab():
    st.markdown(
        """
        <div class="tx-status"><span>9:41</span><span class="tx-signal">● ● ●</span></div>
        <div class="tx-header-row">
            <div class="tx-icon-btn">‹</div>
            <div class="tx-icon-btn">◴</div>
        </div>
        <h1 style="font-size:26px;margin:22px 0 6px;">Learning Leaderboard 🏆</h1>
        <p class="tx-panel-subtitle">
            See who's matching the role today and celebrate the strongest candidates.
        </p>
        <section class="tx-two-grid" style="margin-top:22px;">
            <article class="tx-soft-card" style="background:linear-gradient(135deg,#645cff,#536dff);color:white;text-align:center;">
                <h3 style="margin:0;font-size:22px;color:white;">35%</h3><span>Skill Match</span>
            </article>
            <article class="tx-soft-card" style="background:linear-gradient(135deg,#ffa13a,#ff7d1a);color:white;text-align:center;">
                <h3 style="margin:0;font-size:22px;color:white;">25%</h3><span>Semantic Fit</span>
            </article>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Ranking engine weights"):
        cols = st.columns(5)
        for col, (label, pct) in zip(
            cols,
            [("Skill", 35), ("Semantic", 25), ("Experience", 20), ("Education", 10), ("Keywords", 10)],
        ):
            with col:
                st.progress(pct / 100)
                st.caption(f"{label} {pct}%")

    mode = st.radio(
        "Input mode",
        ["Load sample data", "Enter custom JD + resumes"],
        horizontal=True,
        key="recruiter_mode",
    )

    jd_text = ""
    resumes = []
    if mode == "Load sample data":
        if st.button("Run Sample Ranking", key="sample_rank_btn", use_container_width=True):
            with st.spinner("Loading and ranking 10 candidates..."):
                try:
                    jd_text, resumes = _load_sample_data()
                    st.session_state["ranking_result"] = _direct_rank(jd_text, resumes)
                    st.session_state["ranking_jd"] = jd_text
                except Exception as exc:
                    st.error(f"Ranking error: {exc}")
    else:
        jd_text = st.text_area(
            "Job description",
            height=180,
            placeholder="Paste the full job description here.",
            key="custom_jd",
        )
        count = st.slider("Number of resumes", 2, 8, 3, key="num_resumes")
        for index in range(count):
            with st.expander(f"Resume {index + 1}", expanded=index < 2):
                name = st.text_input(f"Candidate name {index + 1}", key=f"rname_{index}")
                content = st.text_area(f"Resume text {index + 1}", key=f"rcontent_{index}", height=130)
                if name and content:
                    resumes.append({"name": name, "content": content})

        if st.button("Rank Candidates", key="custom_rank_btn", use_container_width=True):
            if not jd_text.strip():
                st.warning("Please enter a job description.")
            elif len(resumes) < 2:
                st.warning("Please add at least 2 complete resumes.")
            else:
                with st.spinner("Ranking candidates..."):
                    try:
                        st.session_state["ranking_result"] = _direct_rank(jd_text, resumes)
                        st.session_state["ranking_jd"] = jd_text
                    except Exception as exc:
                        st.error(f"Ranking error: {exc}")

    if "ranking_result" in st.session_state:
        _render_results(st.session_state["ranking_result"])


def _render_results(result):
    st.markdown(
        f"""
        <section class="tx-leaderboard-card">
            <h2>{result.ranked_candidates[0].total_score:.0f}</h2>
            <p style="margin:6px 0 0;color:white;">Top Match Score</p>
            <span class="tx-pill">100% Ranked</span>
            <div style="font-weight:800;margin-bottom:8px;">{result.ranked_candidates[0].name}</div>
            <div class="tx-podium">
                <div class="tx-step two">2</div>
                <div class="tx-step one">1</div>
                <div class="tx-step three">3</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    top3 = result.ranked_candidates[:3]
    cols = st.columns(len(top3))
    for col, candidate in zip(cols, top3):
        with col:
            st.metric(f"#{_rank_label(candidate.rank)} {candidate.name}", f"{candidate.total_score:.1f}")

    df = pd.DataFrame(
        [
            {
                "Rank": candidate.rank,
                "Name": candidate.name,
                "Total": f"{candidate.total_score:.1f}",
                "Skill": f"{candidate.skill_match:.0f}%",
                "Semantic": f"{candidate.semantic_similarity:.0f}%",
                "Experience": f"{candidate.experience_fit:.0f}%",
                "Education": f"{candidate.education_fit:.0f}%",
            }
            for candidate in result.ranked_candidates
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Export Rankings",
        data=df.to_csv(index=False),
        file_name="talentx_rankings.csv",
        mime="text/csv",
        key="export_csv",
        use_container_width=True,
    )

    st.markdown('<h3 class="tx-panel-title">Score Breakdown</h3>', unsafe_allow_html=True)
    _render_radar_charts(top3)

    st.markdown('<h3 class="tx-panel-title">Candidate Deep Dives</h3>', unsafe_allow_html=True)
    for candidate in result.ranked_candidates:
        with st.expander(f"#{candidate.rank} {candidate.name} · {candidate.total_score:.1f}/100"):
            st.write(candidate.summary)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Matched skills**")
                st.write(", ".join(candidate.matched_skills[:10]) or "None matched")
            with c2:
                st.markdown("**Missing skills**")
                st.write(", ".join(candidate.missing_skills[:8]) or "No critical gaps")


def _render_radar_charts(candidates):
    dimensions = ["Skill", "Semantic", "Experience", "Education", "Keywords"]
    colors = ["#645cff", "#ff971f", "#42bd67"]
    fig = go.Figure()

    for index, candidate in enumerate(candidates):
        values = [
            candidate.skill_match,
            candidate.semantic_similarity,
            candidate.experience_fit,
            candidate.education_fit,
            candidate.keyword_coverage,
        ]
        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=dimensions + [dimensions[0]],
                fill="toself",
                name=candidate.name,
                line_color=colors[index % len(colors)],
                opacity=0.75,
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#edf0fb"),
            angularaxis=dict(gridcolor="#edf0fb"),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#56607d", family="Inter"),
        legend=dict(orientation="h", y=-0.2),
        height=360,
        margin=dict(t=12, b=70, l=28, r=28),
    )
    st.plotly_chart(fig, use_container_width=True)
