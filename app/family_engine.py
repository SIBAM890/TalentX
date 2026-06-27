"""
TalentX – Family Decision Engine
Balances student passion with parent stability concerns.
"""
import re
import logging
from app.models import FamilyDecisionRequest, FamilyDecisionResponse

logger = logging.getLogger("talentx.family")

# Keyword signals for student and parent priorities
STUDENT_SIGNALS = {
    "passion": ["love", "passionate", "dream", "always wanted", "excited", "creative", "art", "music", "startup"],
    "growth": ["grow", "high salary", "future", "career", "opportunity", "global", "abroad", "startup", "research"],
    "freedom": ["independent", "own boss", "freelance", "remote", "travel", "flexible", "freedom"],
    "learning": ["research", "study", "learn", "knowledge", "academia", "phd", "ms", "master"],
}

PARENT_SIGNALS = {
    "stability": ["stable", "security", "safe", "secure", "permanent", "guaranteed", "settled"],
    "proximity": ["home", "near", "close", "local", "same city", "don't go far", "family", "india only"],
    "income": ["salary", "income", "earn", "money", "pay", "support family", "expenses", "loan repay"],
    "reputation": ["reputed", "brand", "good company", "mnc", "bank", "government", "psu", "name"],
}

# Compromise templates based on detected priorities
COMPROMISES = [
    {
        "student_focus": "growth",
        "parent_focus": "stability",
        "compromise": "M.Tech in India (IIT/NIT) + placement in top product company",
        "path": "Pursue M.Tech from IIT/NIT via GATE. High-quality education at low cost, followed by campus placement at top tech companies (₹12–25 LPA). Best of both worlds.",
        "steps": [
            "Prepare for GATE in the final year of B.Tech",
            "Target IIT or NIT for M.Tech in AI/CS",
            "Apply for internships during M.Tech at FAANG/product companies",
            "Land campus placement at ₹12–25 LPA",
            "Start supporting family within 2.5 years"
        ],
        "duration": "3 years total"
    },
    {
        "student_focus": "passion",
        "parent_focus": "income",
        "compromise": "Passion project + stable job (dual track)",
        "path": "Take a stable job to support family while working on your passion project on weekends. Once your side project generates ₹50,000+/month, consider transitioning full-time.",
        "steps": [
            "Accept a stable tech/analyst job (₹4–8 LPA) to cover expenses",
            "Dedicate 2–3 hours daily to passion project",
            "Build an audience or first 10 customers on weekends",
            "Set a milestone: when passion earns ₹50k/month, transition",
            "Keep family informed and involve them in the journey"
        ],
        "duration": "1–3 years to transition"
    },
    {
        "student_focus": "learning",
        "parent_focus": "proximity",
        "compromise": "M.Tech in India + return to home state",
        "path": "Pursue higher studies at a top Indian institute (IIT/NIT/IIIT near home). India now has excellent research programs in AI/ML and CS.",
        "steps": [
            "Research IITs/NITs and IIITs in or near home state",
            "Prepare for GATE or IGATE for admission",
            "Explore fully-funded PhD programs with stipends (₹25,000–35,000/month)",
            "Intern at local tech companies or remote startups during studies",
            "Return home after graduation with ₹12–20 LPA package"
        ],
        "duration": "2–3 years"
    },
    {
        "student_focus": "freedom",
        "parent_focus": "reputation",
        "compromise": "Reputed freelancing + personal brand building",
        "path": "Build a personal brand and freelance at premium rates on reputed platforms (Toptal, Upwork). This combines freedom with credibility.",
        "steps": [
            "Get certified in your niche (AWS, Google, etc.) for credibility",
            "Build 3 strong portfolio projects and publish on GitHub",
            "Join Toptal or Turing (premium, vetted platforms)",
            "Share work publicly on LinkedIn to build reputation",
            "Earn ₹10–30 LPA as a premium freelancer"
        ],
        "duration": "6 months – 1 year"
    },
]

DEFAULT_COMPROMISE = {
    "compromise": "Structured 2-year plan with clear milestones",
    "path": "Create a structured 2-year plan with clear milestones that address both student growth goals and family stability needs. Set quarterly check-ins to evaluate progress.",
    "steps": [
        "Write down both perspectives on paper — student goal vs parent concern",
        "Identify the top 1 non-negotiable for each side",
        "Find careers that satisfy both top priorities",
        "Set a 6-month trial period for the chosen path",
        "Review progress together every 3 months"
    ],
    "duration": "2 years"
}


def _detect_priority(text: str, signals: dict) -> str:
    """Detect dominant priority from text."""
    text_lower = text.lower()
    max_count = 0
    top_priority = list(signals.keys())[0]
    for priority, keywords in signals.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > max_count:
            max_count = count
            top_priority = priority
    return top_priority


def _compute_satisfaction(student_view: str, parent_view: str, compromise: dict) -> tuple[float, float]:
    """Compute how satisfied student and parent would be with the compromise."""
    path_lower = compromise["path"].lower()
    student_signals = sum(1 for kw in ["growth", "opport", "learn", "research", "abroad", "salary", "passion"] if kw in path_lower)
    parent_signals = sum(1 for kw in ["stable", "income", "support", "india", "home", "secure", "reputed", "family"] if kw in path_lower)

    student_sat = min(9.5, 6.0 + student_signals * 0.5)
    parent_sat = min(9.5, 6.0 + parent_signals * 0.5)
    return round(student_sat, 1), round(parent_sat, 1)


class FamilyEngine:
    """Family Decision Mode — balances student vs parent perspectives."""

    def balance_views(self, request: FamilyDecisionRequest) -> FamilyDecisionResponse:
        student_priority = _detect_priority(request.student_view, STUDENT_SIGNALS)
        parent_priority = _detect_priority(request.parent_view, PARENT_SIGNALS)

        # Find best matching compromise
        compromise = DEFAULT_COMPROMISE
        for template in COMPROMISES:
            if (template["student_focus"] == student_priority and
                    template["parent_focus"] == parent_priority):
                compromise = template
                break
            elif (template["student_focus"] == student_priority or
                  template["parent_focus"] == parent_priority):
                compromise = template  # Partial match fallback

        student_sat, parent_sat = _compute_satisfaction(
            request.student_view, request.parent_view, compromise
        )
        compromise_score = round((student_sat + parent_sat) / 2 * 10, 1)

        student_name = request.student_name or "the student"
        key_insight = (
            f"The core tension is between {student_name}'s desire for **{student_priority}** "
            f"and family's need for **{parent_priority}**. "
            f"The compromise path honors both by building stability first while keeping the growth door open."
        )

        return FamilyDecisionResponse(
            student_goal=request.student_view[:200],
            parent_concern=request.parent_view[:200],
            balanced_recommendation=compromise["compromise"],
            compromise_path=compromise["path"],
            student_satisfaction=student_sat,
            parent_satisfaction=parent_sat,
            compromise_score=compromise_score,
            action_steps=compromise["steps"],
            timeline=compromise["duration"],
            key_insight=key_insight,
        )


_family_instance = None


def get_family_engine() -> FamilyEngine:
    global _family_instance
    if _family_instance is None:
        _family_instance = FamilyEngine()
    return _family_instance
