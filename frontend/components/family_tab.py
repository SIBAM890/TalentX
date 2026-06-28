"""Family decision mode UI for TalentX."""
import os
import sys

import plotly.graph_objects as go
import streamlit as st


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def _direct_family(student_view: str, parent_view: str, student_name: str = None):
    from app.family_engine import get_family_engine
    from app.models import FamilyDecisionRequest

    request = FamilyDecisionRequest(
        student_view=student_view,
        parent_view=parent_view,
        student_name=student_name,
    )
    return get_family_engine().balance_views(request)


def render_family_tab():
    st.markdown(
        """
        <div class="tx-status"><span>9:41</span><span class="tx-signal">● ● ●</span></div>
        <div class="tx-header-row">
            <div>
                <h1 style="font-size:25px;margin:0;">Family Decision Mode</h1>
                <p class="tx-panel-subtitle">Balance ambition, stability and family realities.</p>
            </div>
            <div class="tx-icon-btn">◌</div>
        </div>
        <section class="tx-learning-card" style="background:linear-gradient(135deg,#42bd67,#645cff);">
            <div>
                <h3>Find the middle path</h3>
                <p>Student satisfaction + parent confidence + action plan</p>
                <div class="tx-progress-track"><div class="tx-progress-fill" style="width:80%;"></div></div>
            </div>
            <div class="tx-target">◇</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    student_name = st.text_input("Student name", placeholder="Example: Rohan", key="fam_name")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="tx-chip tx-purple-soft">Student View</div>', unsafe_allow_html=True)
        student_view = st.text_area(
            "What does the student want?",
            placeholder="I want to pursue AI research and go abroad for MS...",
            height=155,
            key="fam_student",
            label_visibility="collapsed",
        )
    with col2:
        st.markdown('<div class="tx-chip tx-green-soft">Parent View</div>', unsafe_allow_html=True)
        parent_view = st.text_area(
            "What do parents want?",
            placeholder="We want stability, lower risk, and a job closer to home...",
            height=155,
            key="fam_parent",
            label_visibility="collapsed",
        )

    st.markdown('<h3 class="tx-panel-title">Example Scenarios</h3>', unsafe_allow_html=True)
    scenarios = {
        "MS Abroad vs Job": {
            "student": "I want to pursue AI research and go abroad for MS at a top US university.",
            "parent": "We want you to get a stable job in India near home. Abroad feels too risky.",
        },
        "Startup vs MNC": {
            "student": "I want to start an EdTech company with two co-founders.",
            "parent": "Join a reputed MNC first. Security is important for the family.",
        },
        "UPSC vs Tech": {
            "student": "I want to crack UPSC and become an IAS officer.",
            "parent": "UPSC has no guarantee. Take a tech job first and support the family.",
        },
    }
    cols = st.columns(3)
    for col, (label, data) in zip(cols, scenarios.items()):
        with col:
            if st.button(label, key=f"sc_{label}", use_container_width=True):
                st.session_state["fam_student"] = data["student"]
                st.session_state["fam_parent"] = data["parent"]
                st.rerun()

    if not st.button("Find Balanced Compromise", key="family_btn", use_container_width=True):
        return

    if not student_view.strip() or not parent_view.strip():
        st.warning("Please fill in both the student and parent perspectives.")
        return

    with st.spinner("TalentX is finding the best compromise..."):
        try:
            result = _direct_family(student_view, parent_view, student_name or None)
            _render_family_result(result, student_name or "Student")
        except Exception as exc:
            st.error(f"Family engine error: {exc}")


def _render_family_result(result, student_name: str):
    st.markdown(
        f"""
        <article class="tx-result-card tx-green-soft" style="text-align:center;margin-top:18px;">
            <span style="color:#42bd67;font-size:12px;font-weight:900;">BALANCED RECOMMENDATION</span>
            <h3 style="margin:8px 0;">{result.balanced_recommendation}</h3>
            <h2 style="margin:8px 0 0;color:#42bd67;">{result.compromise_score:.0f}%</h2>
            <p class="tx-panel-subtitle" style="margin-top:0;">Compromise score</p>
        </article>
        <article class="tx-result-card tx-purple-soft" style="margin-top:14px;">
            <span style="color:#645cff;font-size:12px;font-weight:900;">KEY INSIGHT</span>
            <p style="margin:8px 0 0;">{result.key_insight}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        _render_satisfaction_gauge(result.student_satisfaction, f"{student_name}", "#645cff")
    with c2:
        _render_satisfaction_gauge(result.parent_satisfaction, "Parents", "#42bd67")

    st.markdown('<h3 class="tx-panel-title">Compromise Path</h3>', unsafe_allow_html=True)
    st.info(result.compromise_path)

    st.markdown('<h3 class="tx-panel-title">Action Steps</h3>', unsafe_allow_html=True)
    for index, step in enumerate(result.action_steps, 1):
        st.markdown(
            f"""
            <article class="tx-result-card" style="display:flex;gap:12px;align-items:center;margin:8px 0;padding:12px;">
                <strong style="display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#645cff;color:white;">{index}</strong>
                <span>{step}</span>
            </article>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(f"**Estimated timeline:** {result.timeline}")


def _render_satisfaction_gauge(score: float, label: str, color: str):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "/10", "font": {"size": 25, "color": color, "family": "Inter"}},
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": label, "font": {"size": 13, "color": "#56607d", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#c5cbe0"},
                "bar": {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 4], "color": "#fff0f6"},
                    {"range": [4, 7], "color": "#fff1e4"},
                    {"range": [7, 10], "color": "#edf9ef"},
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#56607d", family="Inter"),
        height=220,
        margin=dict(t=38, b=8, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)
