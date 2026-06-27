"""
TalentX – Family Mode Tab
Balance student passion with parent stability concerns.
"""
import streamlit as st
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def _direct_family(student_view: str, parent_view: str, student_name: str = None):
    from app.family_engine import get_family_engine
    from app.models import FamilyDecisionRequest
    engine = get_family_engine()
    req = FamilyDecisionRequest(
        student_view=student_view,
        parent_view=parent_view,
        student_name=student_name,
    )
    return engine.balance_views(req)


def render_family_tab():
    """Render the Family Mode tab."""

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(67,217,179,0.12), rgba(108,99,255,0.08));
                border: 1px solid rgba(67,217,179,0.3); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;'>
        <h2 style='margin:0; color:#43D9B3; font-family: Outfit, sans-serif;'>👨‍👩‍👧 Family Decision Mode</h2>
        <p style='margin:0.3rem 0 0 0; color: #9999BB; font-size: 0.95rem;'>
        India's career decisions are family decisions. TalentX balances both perspectives and finds the optimal compromise.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Inputs ──────────────────────────────────────────────────────────────────
    name_col, _ = st.columns([1, 3])
    with name_col:
        student_name = st.text_input("👤 Student's Name (optional)", placeholder="e.g., Rohan", key="fam_name")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background: rgba(108,99,255,0.08); border-left: 3px solid #6C63FF;
                    border-radius: 0 10px 10px 0; padding: 0.5rem 0.75rem; margin-bottom: 0.5rem;'>
            <span style='color: #6C63FF; font-weight: 700; font-size: 0.9rem;'>🎓 Student's Perspective</span>
        </div>
        """, unsafe_allow_html=True)
        student_view = st.text_area(
            "What does the student want?",
            placeholder="e.g., I want to pursue AI research and go abroad for MS. I'm passionate about machine learning and want to work at Google eventually.",
            height=160,
            key="fam_student",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("""
        <div style='background: rgba(67,217,179,0.08); border-left: 3px solid #43D9B3;
                    border-radius: 0 10px 10px 0; padding: 0.5rem 0.75rem; margin-bottom: 0.5rem;'>
            <span style='color: #43D9B3; font-weight: 700; font-size: 0.9rem;'>👨‍👩‍👧 Parent's Perspective</span>
        </div>
        """, unsafe_allow_html=True)
        parent_view = st.text_area(
            "What do parents want?",
            placeholder="e.g., We want him to get a stable job near home. The family has loans. We're worried about visa and living abroad. A government job or MNC would be perfect.",
            height=160,
            key="fam_parent",
            label_visibility="collapsed",
        )

    # ── Example Scenarios ──────────────────────────────────────────────────────
    st.markdown("**💡 Load an example scenario:**")
    scenarios = {
        "🎓 MS Abroad vs Stable Job": {
            "student": "I want to pursue AI research and go abroad for MS at a top US university. I want to work at Google or Meta.",
            "parent": "We want you to get a stable job in India near home. We have EMI and family responsibilities. Abroad is too risky."
        },
        "🚀 Startup vs MNC": {
            "student": "I want to start my own startup in EdTech. I have a strong idea and 2 co-founders ready.",
            "parent": "We want you to join a reputed MNC like TCS or Infosys. Get 5 years experience then think of startup. Security is important."
        },
        "🏛️ UPSC vs Tech Job": {
            "student": "I'm passionate about public service. I want to crack UPSC and become an IAS officer. It's my dream.",
            "parent": "UPSC takes 5 years and there is no guarantee. Take a tech job first. The salary will help the family immediately."
        },
    }
    sc_cols = st.columns(3)
    for col, (label, data) in zip(sc_cols, scenarios.items()):
        with col:
            if st.button(label, key=f"sc_{label}", use_container_width=True):
                st.session_state["fam_student"] = data["student"]
                st.session_state["fam_parent"] = data["parent"]
                st.rerun()

    st.markdown("---")
    analyze_btn = st.button("⚖️ Find Balanced Compromise", key="family_btn", use_container_width=True)

    if not analyze_btn:
        return

    if not student_view.strip() or not parent_view.strip():
        st.warning("Please fill in both the student and parent perspectives.")
        return

    with st.spinner("🤖 TalentX is finding the best compromise..."):
        try:
            result = _direct_family(student_view, parent_view, student_name or None)
            _render_family_result(result, student_name or "Student")
        except Exception as e:
            st.error(f"Family engine error: {e}")


def _render_family_result(result, student_name: str):
    """Render family decision result."""

    # ── Compromise Score Banner ────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(67,217,179,0.15), rgba(108,99,255,0.12));
                border: 1px solid rgba(67,217,179,0.4); border-radius: 16px; padding: 1.5rem 2rem; margin: 1rem 0;
                text-align: center;'>
        <div style='color: #9999BB; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em;'>
            BALANCED RECOMMENDATION
        </div>
        <div style='color: #F0F0FF; font-size: 1.4rem; font-weight: 700; margin: 0.5rem 0;'>
            {result.balanced_recommendation}
        </div>
        <div style='color: #43D9B3; font-size: 2rem; font-weight: 800;'>
            {result.compromise_score:.0f}%
        </div>
        <div style='color: #9999BB; font-size: 0.8rem;'>Compromise Score</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Insight ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background: rgba(108,99,255,0.08); border-left: 4px solid #6C63FF;
                border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin: 1rem 0;'>
        <span style='color: #9999BB; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em;'>💡 KEY INSIGHT</span>
        <div style='color: #F0F0FF; margin-top: 0.4rem;'>{result.key_insight}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Satisfaction Gauges ────────────────────────────────────────────────────
    st.markdown("#### 😊 Satisfaction Scores")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        _render_satisfaction_gauge(
            result.student_satisfaction,
            f"🎓 {student_name}'s Satisfaction",
            "#6C63FF"
        )

    with g_col2:
        _render_satisfaction_gauge(
            result.parent_satisfaction,
            "👨‍👩‍👧 Parent's Satisfaction",
            "#43D9B3"
        )

    # ── Compromise Path ────────────────────────────────────────────────────────
    st.markdown("#### 🛤️ The Compromise Path")
    st.info(result.compromise_path)

    # ── Action Steps ──────────────────────────────────────────────────────────
    st.markdown("#### ✅ Action Steps")
    for i, step in enumerate(result.action_steps, 1):
        st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0;
                    border-bottom: 1px solid rgba(255,255,255,0.05);'>
            <span style='background: linear-gradient(135deg, #6C63FF, #FF6584); color: white;
                         border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center;
                         justify-content: center; font-size: 0.75rem; font-weight: 700; min-width: 24px;'>{i}</span>
            <span style='color: #F0F0FF;'>{step}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Timeline ──────────────────────────────────────────────────────────────
    st.markdown(f"**⏱️ Estimated Timeline:** {result.timeline}")


def _render_satisfaction_gauge(score: float, label: str, color: str):
    """Render a circular gauge for satisfaction score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "/10", "font": {"size": 28, "color": color, "family": "Inter"}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": label, "font": {"size": 13, "color": "#9999BB", "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#9999BB"},
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 4], "color": "rgba(255,101,132,0.1)"},
                {"range": [4, 7], "color": "rgba(255,193,7,0.1)"},
                {"range": [7, 10], "color": "rgba(67,217,179,0.1)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.85,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9999BB", family="Inter"),
        height=230,
        margin=dict(t=40, b=10, l=30, r=30),
    )
    st.plotly_chart(fig, use_container_width=True)
