"""Candidate mode UI for TalentX."""
import os
import sys

import plotly.graph_objects as go
import requests
import streamlit as st


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.config import API_BASE_URL


def _api(endpoint: str, payload: dict = None, method: str = "POST"):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=payload, timeout=30)
        else:
            response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _direct_decide(query: str, background: str = None, location: str = None):
    from app.decision_engine import get_decision_engine
    from app.models import CandidateDecisionRequest

    engine = get_decision_engine()
    request = CandidateDecisionRequest(query=query, user_background=background, location=location)
    return engine.simulate_options(request)


def _direct_risk(option: str, profile: str = None):
    from app.models import RiskRequest
    from app.risk_engine import get_risk_engine

    engine = get_risk_engine()
    request = RiskRequest(option=option, user_profile=profile)
    return engine.assess_risk(request.option, request.user_profile)


def _direct_scholarships(state: str):
    from app.bharat_knowledge import get_bharat_knowledge

    return get_bharat_knowledge().get_scholarships(state=state)


def _option_color(index: int) -> str:
    return ["#645cff", "#ff971f", "#42bd67", "#f25584"][index % 4]


def render_candidate_tab():
    st.markdown(
        """
        <div class="tx-status"><span>9:41</span><span class="tx-signal">● ● ●</span></div>
        <div class="tx-header-row">
            <div class="tx-avatar">A</div>
            <div style="flex:1; padding-left:12px;">
                <h2 style="margin:0;font-size:18px;">Hi, Ananya!</h2>
                <p class="tx-panel-subtitle" style="margin-top:3px;">What career path do you want to explore today?</p>
            </div>
            <div class="tx-icon-btn">⌁</div>
        </div>
        <section class="tx-learning-card">
            <div>
                <h3>Your Learning Journey</h3>
                <p>Level 3 · Keep learning!</p>
                <div class="tx-progress-track"><div class="tx-progress-fill"></div></div>
            </div>
            <div class="tx-target">◎</div>
        </section>
        <h3 class="tx-panel-title">My Learning Plan</h3>
        <section class="tx-stat-grid" style="grid-template-columns:repeat(3,1fr);">
            <article class="tx-stat tx-green-soft"><i>▰</i><strong>15</strong><span>Career Paths</span></article>
            <article class="tx-stat tx-orange-soft"><i>□</i><strong>4</strong><span>Risk Types</span></article>
            <article class="tx-stat tx-blue-soft"><i>▣</i><strong>50+</strong><span>Schemes</span></article>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h3 class="tx-panel-title">Quick Activities</h3>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown(
            '<article class="tx-soft-card tx-activity purple"><strong>Compare Paths</strong><br>'
            '<span>See cost, growth, time and risk together</span></article>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            '<article class="tx-soft-card tx-activity orange"><strong>Smart Focus</strong><br>'
            '<span>Find safer choices and action steps</span></article>',
            unsafe_allow_html=True,
        )

    query = st.text_area(
        "Career dilemma",
        placeholder="Example: I am a BTech CSE student confused between GATE, placements, and MS abroad.",
        height=112,
        key="candidate_query",
    )
    background = st.text_area(
        "Background",
        placeholder="Example: 3rd year BTech, CGPA 8.0, Python and ML basics.",
        height=82,
        key="candidate_bg",
    )
    location = st.text_input("State", placeholder="Example: Odisha", key="candidate_location")

    if not st.button("Simulate My Options", key="analyze_btn", use_container_width=True):
        _render_example_prompts()
        return

    if not query.strip():
        st.warning("Please enter your career question above.")
        return

    with st.spinner("TalentX is simulating your options..."):
        try:
            result = _direct_decide(query.strip(), background or None, location or None)
            _render_results(result, location)
        except Exception as exc:
            st.error(f"Error: {exc}")


def _render_example_prompts():
    st.markdown(
        """
        <section class="tx-chip-row">
            <span class="tx-chip tx-purple-soft">GATE vs Job</span>
            <span class="tx-chip tx-orange-soft">MBA vs DS</span>
            <span class="tx-chip tx-green-soft">Startup Risk</span>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_results(result, location: str = None):
    options = result.options
    if not options:
        st.error("No options detected. Please rephrase your query.")
        return

    st.markdown(
        f"""
        <article class="tx-result-card tx-purple-soft" style="margin-top:18px;">
            <span style="color:#645cff;font-size:12px;font-weight:900;">AI RECOMMENDATION</span>
            <h3 style="margin:8px 0 0;">{result.recommendation}</h3>
        </article>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h3 class="tx-panel-title">Options Comparison</h3>', unsafe_allow_html=True)
    _render_comparison_chart(options)

    st.markdown('<h3 class="tx-panel-title">Detailed Analysis</h3>', unsafe_allow_html=True)
    for index, option in enumerate(options):
        with st.expander(f"{index + 1}. {option.name} · {option.confidence:.0f}%", expanded=index == 0):
            c1, c2, c3 = st.columns(3)
            c1.metric("Cost", option.cost.split("(")[0].strip())
            c2.metric("Time", option.time_required)
            c3.metric("Risk", option.risk_level)
            st.markdown(f"**Expected salary:** {option.expected_salary}")
            st.write(option.description)

            pcol1, pcol2 = st.columns(2)
            with pcol1:
                st.markdown("**Pros**")
                for pro in option.pros:
                    st.markdown(f"- {pro}")
            with pcol2:
                st.markdown("**Cons**")
                for con in option.cons:
                    st.markdown(f"- {con}")

            if option.timeline:
                st.markdown("**Roadmap**")
                for milestone in option.timeline[:5]:
                    st.markdown(f"**Year {milestone.year}:** {milestone.milestone} → {milestone.action}")

    st.markdown('<h3 class="tx-panel-title">Risk Intelligence</h3>', unsafe_allow_html=True)
    try:
        _render_risk_panel(_direct_risk(options[0].name, None))
    except Exception:
        st.info("Risk analysis unavailable.")

    if location:
        st.markdown('<h3 class="tx-panel-title">Bharat Knowledge Layer</h3>', unsafe_allow_html=True)
        try:
            _render_scholarships(_direct_scholarships(location))
        except Exception:
            pass


def _render_comparison_chart(options):
    if len(options) < 2:
        return

    fig = go.Figure()
    for index, option in enumerate(options):
        fig.add_trace(
            go.Bar(
                name=option.name[:24],
                x=["Cost", "Growth", "Confidence"],
                y=[option.cost_score, option.growth_score, option.confidence],
                marker_color=_option_color(index),
                opacity=0.9,
            )
        )

    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#56607d", family="Inter"),
        yaxis=dict(range=[0, 100], gridcolor="#edf0fb"),
        xaxis=dict(gridcolor="#edf0fb"),
        legend=dict(orientation="h", y=-0.22),
        height=300,
        margin=dict(t=6, b=58, l=0, r=0),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_risk_panel(risk):
    st.markdown(
        f"""
        <article class="tx-result-card tx-orange-soft">
            <span style="color:#ff7d00;font-size:12px;font-weight:900;">OVERALL RISK</span>
            <h2 style="margin:6px 0 0;">{risk.overall_risk} · {risk.overall_score:.0f}/100</h2>
        </article>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(risk.risks))
    for col, item in zip(cols, risk.risks):
        with col:
            st.metric(item.risk_type, f"{item.score:.0f}", item.level)

    if risk.safer_alternatives:
        st.markdown("**Safer alternatives**")
        for alternative in risk.safer_alternatives[:3]:
            st.markdown(f"- {alternative}")


def _render_scholarships(scholarships):
    st.info(f"Found {scholarships.total_found} scholarships for {scholarships.state}.")
    tabs = st.tabs(["Central", "State", "Private"])
    with tabs[0]:
        for item in scholarships.central_schemes[:4]:
            st.markdown(f"**{item.name}** · {item.amount} · {item.eligibility}")
    with tabs[1]:
        for item in scholarships.state_schemes[:4]:
            st.markdown(f"**{item.name}** · {item.amount}")
    with tabs[2]:
        for item in scholarships.private_scholarships[:3]:
            st.markdown(f"**{item.name}** · {item.amount}")
