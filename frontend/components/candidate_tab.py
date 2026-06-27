"""
TalentX – Candidate Tab (DishaSetu Mode)
Career decision simulator for Indian students.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.config import API_BASE_URL


def _api(endpoint: str, payload: dict = None, method: str = "POST"):
    """Make API call with fallback to direct engine call."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "POST":
            r = requests.post(url, json=payload, timeout=30)
        else:
            r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


def _direct_decide(query: str, background: str = None, location: str = None):
    """Direct engine call bypassing HTTP (fallback)."""
    from app.decision_engine import get_decision_engine
    from app.models import CandidateDecisionRequest
    engine = get_decision_engine()
    req = CandidateDecisionRequest(query=query, user_background=background, location=location)
    return engine.simulate_options(req)


def _direct_risk(option: str, profile: str = None):
    from app.risk_engine import get_risk_engine
    from app.models import RiskRequest
    engine = get_risk_engine()
    req = RiskRequest(option=option, user_profile=profile)
    return engine.assess_risk(req.option, req.user_profile)


def _direct_scholarships(state: str):
    from app.bharat_knowledge import get_bharat_knowledge
    knowledge = get_bharat_knowledge()
    return knowledge.get_scholarships(state=state)


def _option_color(idx: int) -> str:
    colors = ["#6C63FF", "#FF6584", "#43D9B3", "#FFC107"]
    return colors[idx % len(colors)]


def render_candidate_tab():
    """Main render function for the Candidate / DishaSetu tab."""

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(67,217,179,0.08));
                border: 1px solid rgba(108,99,255,0.3); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;'>
        <h2 style='margin:0; color:#6C63FF; font-family: Outfit, sans-serif;'>🧭 DishaSetu Mode</h2>
        <p style='margin:0.3rem 0 0 0; color: #9999BB; font-size: 0.95rem;'>
        AI-powered career decision simulator for Indian students. Compare paths, assess risks, visualize futures.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input ──────────────────────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_area(
            "🎯 What's your career dilemma?",
            placeholder="e.g., I'm a BTech CSE student confused between GATE, placements, and higher studies abroad...",
            height=110,
            key="candidate_query"
        )
    with col2:
        background = st.text_area(
            "👤 Your Background (optional)",
            placeholder="e.g., 3rd year BTech, CGPA 8.0, know Python & ML basics",
            height=55,
            key="candidate_bg"
        )
        location = st.text_input(
            "📍 Your State (optional)",
            placeholder="e.g., Odisha, Maharashtra",
            key="candidate_location"
        )

    analyze_btn = st.button("🚀 Simulate My Options", key="analyze_btn", use_container_width=True)

    if not analyze_btn:
        _render_example_prompts()
        return

    if not query.strip():
        st.warning("Please enter your career question above.")
        return

    with st.spinner("🤖 TalentX is simulating your options..."):
        try:
            result = _direct_decide(query.strip(), background or None, location or None)
            _render_results(result, location)
        except Exception as e:
            st.error(f"Error: {e}")


def _render_example_prompts():
    st.markdown("---")
    st.markdown("#### 💡 Try these examples:")
    examples = [
        "I'm a BTech CSE student confused between GATE, placements, and higher studies abroad",
        "Should I do MBA or pursue data science after my engineering?",
        "I want to start a startup vs get a stable job — help me decide",
        "I'm from Odisha, confused between government jobs and private tech companies",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        with cols[i % 2]:
            st.markdown(f"""
            <div style='background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2);
                        border-radius: 10px; padding: 0.75rem; margin: 0.3rem 0; cursor: pointer;
                        font-size: 0.85rem; color: #9999BB;'>
            💬 "{ex[:80]}..."
            </div>
            """, unsafe_allow_html=True)


def _render_results(result, location: str = None):
    options = result.options
    if not options:
        st.error("No options detected. Please rephrase your query.")
        return

    # ── Recommendation Banner ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(67,217,179,0.1));
                border: 1px solid rgba(108,99,255,0.4); border-radius: 14px; padding: 1.2rem 1.5rem; margin: 1rem 0;'>
        <div style='color: #6C63FF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;'>
            🏆 AI RECOMMENDATION
        </div>
        <div style='color: #F0F0FF; font-size: 1rem; margin-top: 0.4rem;'>{result.recommendation}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Options Comparison Table ───────────────────────────────────────────────
    st.markdown("### 📊 Options Comparison")
    _render_comparison_chart(options)

    # ── Individual Option Cards ────────────────────────────────────────────────
    st.markdown("### 🔍 Detailed Analysis")
    for idx, opt in enumerate(options):
        color = _option_color(idx)
        with st.expander(f"{'🥇' if idx==0 else '🥈' if idx==1 else '🥉' if idx==2 else '📌'} **{opt.name}** — Score: {opt.confidence:.0f}%", expanded=(idx == 0)):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("💰 Cost", opt.cost.split("(")[0].strip())
            with c2:
                st.metric("⏱️ Time", opt.time_required)
            with c3:
                risk_emoji = "🟢" if opt.risk_level == "Low" else "🟡" if opt.risk_level == "Medium" else "🔴"
                st.metric(f"{risk_emoji} Risk", opt.risk_level)
            with c4:
                st.metric("📈 Growth", opt.growth_potential)

            st.markdown(f"**💼 Expected Salary:** {opt.expected_salary}")
            st.markdown(f"*{opt.description}*")

            # Pros / Cons
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                st.markdown("**✅ Pros:**")
                for pro in opt.pros:
                    st.markdown(f"- {pro}")
            with pcol2:
                st.markdown("**⚠️ Cons:**")
                for con in opt.cons:
                    st.markdown(f"- {con}")

            # Timeline
            if opt.timeline:
                st.markdown("**📅 Year-by-Year Roadmap:**")
                for m in opt.timeline[:5]:
                    st.markdown(f"**Year {m.year}** · {m.milestone} → *{m.action}*")

    # ── Risk Assessment ────────────────────────────────────────────────────────
    if options:
        st.markdown("---")
        st.markdown("### 🛡️ Risk Intelligence")
        with st.spinner("Assessing risks..."):
            try:
                risk = _direct_risk(options[0].name, None)
                _render_risk_panel(risk)
            except Exception as e:
                st.info("Risk analysis unavailable.")

    # ── Bharat Scholarships ────────────────────────────────────────────────────
    if location:
        st.markdown("---")
        st.markdown("### 🇮🇳 Bharat Knowledge Layer")
        with st.spinner("Fetching scholarships..."):
            try:
                scholarships = _direct_scholarships(location)
                _render_scholarships(scholarships)
            except Exception:
                pass


def _render_comparison_chart(options):
    """Render a radar/bar chart comparing all options."""
    if len(options) < 2:
        return

    categories = ["Cost", "Growth", "Confidence"]
    fig = go.Figure()

    for i, opt in enumerate(options):
        color = _option_color(i)
        fig.add_trace(go.Bar(
            name=opt.name[:30],
            x=categories,
            y=[opt.cost_score, opt.growth_score, opt.confidence],
            marker_color=color,
            marker_line_color="rgba(255,255,255,0.1)",
            marker_line_width=1,
            opacity=0.85,
        ))

    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9999BB", family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#9999BB")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#9999BB"), range=[0, 100]),
        height=300,
        margin=dict(t=10, b=10, l=0, r=0),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_risk_panel(risk):
    """Render risk assessment panel."""
    overall_color = "#43D9B3" if risk.overall_risk == "Low" else "#FFC107" if risk.overall_risk == "Medium" else "#FF6584"

    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1rem;'>
        <span style='color: {overall_color}; font-size: 1.3rem; font-weight: 800;'>
            Overall Risk: {risk.overall_risk} ({risk.overall_score:.0f}/100)
        </span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(risk.risks))
    for i, r in enumerate(risk.risks):
        color = "#43D9B3" if r.level == "Low" else "#FFC107" if r.level == "Medium" else "#FF6584"
        with cols[i]:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); border: 1px solid {color}30;
                        border-radius: 10px; padding: 0.8rem; text-align: center;'>
                <div style='color: {color}; font-weight: 700; font-size: 0.9rem;'>{r.risk_type}</div>
                <div style='font-size: 1.5rem; font-weight: 800; color: {color};'>{r.score:.0f}</div>
                <div style='color: #9999BB; font-size: 0.75rem;'>{r.level}</div>
            </div>
            """, unsafe_allow_html=True)

    if risk.safer_alternatives:
        st.markdown("**💡 Safer Alternatives:**")
        for alt in risk.safer_alternatives[:3]:
            st.markdown(f"- {alt}")


def _render_scholarships(scholarships):
    """Render scholarship cards."""
    total = scholarships.total_found
    st.info(f"🎓 Found {total} scholarships for **{scholarships.state}**")

    tabs = st.tabs(["🏛️ Central Schemes", "🗺️ State Schemes", "🏢 Private"])
    with tabs[0]:
        for s in scholarships.central_schemes[:4]:
            st.markdown(f"**{s.name}** · {s.amount} · *{s.eligibility}*")
            st.markdown(f"[Apply Here]({s.apply_at}) | Limit: {s.income_limit}")
            st.divider()
    with tabs[1]:
        for s in scholarships.state_schemes[:4]:
            st.markdown(f"**{s.name}** · {s.amount}")
            st.markdown(f"[Apply Here]({s.apply_at})")
            st.divider()
    with tabs[2]:
        for s in scholarships.private_scholarships[:3]:
            st.markdown(f"**{s.name}** · {s.amount}")
            st.markdown(f"[Apply Here]({s.apply_at})")
            st.divider()
