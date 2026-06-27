"""
TalentX – Main Streamlit Application
The X Factor in Hiring & Life Decisions
"""
import streamlit as st
import sys
import os

# Ensure the repo root is on path so app/ is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentX – The X Factor in Hiring & Life Decisions",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/talentx",
        "About": "TalentX – Built for India Runs Hackathon by Redrob AI",
    },
)

# ── Load Custom CSS ────────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Import Tab Components ──────────────────────────────────────────────────────
from frontend.components.candidate_tab import render_candidate_tab
from frontend.components.recruiter_tab import render_recruiter_tab
from frontend.components.family_tab import render_family_tab


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 2.5rem;'>🚀</div>
        <div style='font-family: Outfit, sans-serif; font-size: 1.4rem; font-weight: 700;
                    background: linear-gradient(135deg, #6C63FF, #FF6584);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;'>TalentX</div>
        <div style='color: #9999BB; font-size: 0.75rem; letter-spacing: 0.08em;'>
            THE X FACTOR IN HIRING & LIFE DECISIONS
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='color: #9999BB; font-size: 0.78rem; text-transform: uppercase;
                letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;'>
        Platform Features
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("🧭", "DishaSetu Mode", "Career Decision Simulator"),
        ("📊", "TalentX Mode", "Candidate Ranking Engine"),
        ("👨‍👩‍👧", "Family Mode", "Balance Views & Compromise"),
        ("🇮🇳", "Bharat Layer", "India Scholarships & Data"),
        ("🛡️", "Risk Engine", "4-Dimension Risk Analysis"),
        ("📅", "Timeline Engine", "Year-by-Year Roadmaps"),
    ]

    for icon, name, desc in features:
        st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.3rem;
                    border-radius: 8px; margin: 0.15rem 0;'>
            <span style='font-size: 1rem;'>{icon}</span>
            <div>
                <div style='color: #F0F0FF; font-size: 0.85rem; font-weight: 600;'>{name}</div>
                <div style='color: #9999BB; font-size: 0.72rem;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Stats
    st.markdown("""
    <div style='color: #9999BB; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;'>
        Platform Stats
    </div>
    """, unsafe_allow_html=True)

    stats = [("200+", "Skills in Taxonomy"), ("15", "Career Paths"), ("50+", "Scholarships"), ("10", "Sample Resumes")]
    for val, label in stats:
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center;
                    padding: 0.35rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);'>
            <span style='color: #9999BB; font-size: 0.8rem;'>{label}</span>
            <span style='color: #6C63FF; font-weight: 700; font-size: 0.9rem;'>{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # API Status
    st.markdown("**🔌 API Status**")
    try:
        from app.decision_engine import get_decision_engine
        get_decision_engine()  # Light check
        st.markdown("<span style='color: #43D9B3; font-weight: 600;'>● Engines Online</span>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<span style='color: #FF6584;'>● Engine Loading...</span>", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style='color: #9999BB; font-size: 0.72rem; text-align: center;'>
        Built for <strong style='color: #6C63FF;'>India Runs Hackathon</strong><br>
        by Redrob AI | Track 1: Data & AI
    </div>
    """, unsafe_allow_html=True)


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem 1.5rem;'>
    <div style='display: inline-block; background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.3);
                border-radius: 999px; padding: 0.3rem 1rem; margin-bottom: 1rem;
                color: #6C63FF; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.08em;'>
        🏆 INDIA RUNS HACKATHON · REDROB AI · TRACK 1: DATA & AI
    </div>
    <h1 style='font-family: Outfit, sans-serif; font-size: 3rem; font-weight: 800; margin: 0;
               background: linear-gradient(135deg, #6C63FF 0%, #FF6584 50%, #43D9B3 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
        TalentX
    </h1>
    <p style='color: #9999BB; font-size: 1.1rem; margin: 0.3rem 0;
              font-style: italic; letter-spacing: 0.03em;'>
        "Not filters. Not advice. <strong style='color: #F0F0FF;'>Intelligence.</strong>"
    </p>
    <p style='color: #666688; font-size: 0.85rem; margin-top: 0.5rem;'>
        The X Factor in Hiring & Life Decisions · Built for India 🇮🇳
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI Strip ─────────────────────────────────────────────────────────────────
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpis = [
    ("98%", "Resumes Rejected by ATS", "#FF6584"),
    ("6 sec", "Time Spent on a Resume", "#FFC107"),
    ("70%", "Hidden Gems Missed", "#6C63FF"),
    ("1.4B", "Indians Deserve Better", "#43D9B3"),
    ("₹50L+", "Prize Pool at Stake", "#FF6584"),
]
for col, (val, label, color) in zip([kpi1, kpi2, kpi3, kpi4, kpi5], kpis):
    with col:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
                    border-radius: 12px; padding: 0.9rem; text-align: center;'>
            <div style='font-size: 1.6rem; font-weight: 800; color: {color};
                        font-family: Outfit, sans-serif;'>{val}</div>
            <div style='color: #9999BB; font-size: 0.7rem; margin-top: 0.2rem;
                        text-transform: uppercase; letter-spacing: 0.06em;'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🧭 Candidate – DishaSetu Mode",
    "📊 Recruiter – TalentX Mode",
    "👨‍👩‍👧 Family Decision Mode",
])

with tab1:
    render_candidate_tab()

with tab2:
    render_recruiter_tab()

with tab3:
    render_family_tab()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666688; font-size: 0.8rem; padding: 1rem;'>
    Built with ❤️ for India · India Runs Hackathon by Redrob AI · 
    <strong style='color: #6C63FF;'>TalentX</strong> – The X Factor in Hiring & Life Decisions<br>
    <span style='font-size: 0.72rem;'>
        Tech Stack: FastAPI · Sentence-BERT · spaCy · scikit-learn · Streamlit · Plotly
    </span>
</div>
""", unsafe_allow_html=True)
