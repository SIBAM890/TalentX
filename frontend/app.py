"""
TalentX Streamlit frontend.

The interface is intentionally styled like the supplied mobile app mockups:
soft white surface, rounded pastel cards, purple/orange actions, and a
bottom-navigation feel.
"""
import os
import sys

import streamlit as st


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.candidate_tab import render_candidate_tab
from frontend.components.family_tab import render_family_tab
from frontend.components.recruiter_tab import render_recruiter_tab


st.set_page_config(
    page_title="TalentX",
    page_icon="TX",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com/yourusername/talentx",
        "About": "TalentX - The X Factor in Hiring & Life Decisions",
    },
)


css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_home_screen() -> None:
    st.markdown(
        """
        <section class="tx-hero">
            <div class="tx-status">
                <span>9:41</span>
                <span class="tx-signal">● ● ●</span>
            </div>
            <div class="tx-topbar">
                <div>
                    <h1>TalentX</h1>
                    <p>The X Factor in Hiring &amp; Life Decisions</p>
                </div>
                <div class="tx-icon-btn">⌁</div>
            </div>
            <div class="tx-spark tx-spark-a"></div>
            <div class="tx-spark tx-spark-b"></div>
            <div class="tx-people" aria-hidden="true">
                <div class="tx-person tx-person-left">
                    <div class="tx-face"></div><div class="tx-book"></div>
                </div>
                <div class="tx-person tx-person-main">
                    <div class="tx-face"></div><div class="tx-laptop"></div>
                </div>
                <div class="tx-person tx-person-right">
                    <div class="tx-face"></div><div class="tx-book"></div>
                </div>
            </div>
            <h2>AI-Powered Guidance for Smarter Decisions</h2>
            <p class="tx-subtitle">
                Career decisions, risk analysis, scholarships and intelligent hiring,
                all in one place.
            </p>
        </section>

        <section class="tx-mode-grid">
            <article class="tx-mode-card tx-purple-soft">
                <div class="tx-card-icon">◈</div>
                <strong>Candidate Mode</strong>
                <span>Career guidance &amp; decision making</span>
                <b>›</b>
            </article>
            <article class="tx-mode-card tx-orange-soft">
                <div class="tx-card-icon tx-orange-text">▣</div>
                <strong>Recruiter Mode</strong>
                <span>Candidate ranking &amp; insights</span>
                <b>›</b>
            </article>
        </section>

        <h3 class="tx-section-title">Platform Highlights</h3>
        <section class="tx-stat-grid">
            <article class="tx-stat tx-purple-soft"><i>◆</i><strong>15+</strong><span>Career Paths</span></article>
            <article class="tx-stat tx-green-soft"><i>▰</i><strong>200+</strong><span>Skills</span></article>
            <article class="tx-stat tx-pink-soft"><i>●</i><strong>50+</strong><span>Scholarships</span></article>
            <article class="tx-stat tx-blue-soft"><i>●●</i><strong>1000+</strong><span>Resumes</span></article>
        </section>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<main class="tx-phone-shell">', unsafe_allow_html=True)
home_tab, candidate_tab, recruiter_tab, family_tab = st.tabs(
    ["Home", "Plan", "Leaderboard", "Family"]
)

with home_tab:
    render_home_screen()

with candidate_tab:
    render_candidate_tab()

with recruiter_tab:
    render_recruiter_tab()

with family_tab:
    render_family_tab()

st.markdown(
    """
    <nav class="tx-bottom-nav" aria-hidden="true">
        <span class="active">⌂<small>Home</small></span>
        <span>□<small>Plan</small></span>
        <span>♕<small>Rank</small></span>
        <span>○<small>Profile</small></span>
    </nav>
    """,
    unsafe_allow_html=True,
)
st.markdown("</main>", unsafe_allow_html=True)
