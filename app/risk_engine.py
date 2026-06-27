"""
TalentX – Risk Intelligence Engine
Detects financial, skill gap, market, and time risks.
"""
import re
import logging
from app.models import RiskItem, RiskResponse
from app.utils import get_risk_label

logger = logging.getLogger("talentx.risk")

# Risk signals (keywords → risk type → base score bump)
RISK_SIGNALS = {
    "financial": {
        "keywords": [
            "dropout", "drop out", "quit", "no savings", "loan", "debt", "borrow",
            "expensive", "costly", "abroad", "foreign", "startup", "no income",
            "family depends", "sole earner", "poor", "below poverty"
        ],
        "base_score": 30,
        "bump": 15,
    },
    "skill_gap": {
        "keywords": [
            "no experience", "beginner", "never done", "don't know", "confused",
            "no skills", "fresher", "just started", "new to", "zero experience",
            "changing field", "switching", "different domain", "no background"
        ],
        "base_score": 30,
        "bump": 12,
    },
    "market": {
        "keywords": [
            "saturated", "competitive", "many candidates", "low demand", "niche",
            "outdated", "old technology", "declining", "no jobs", "few openings",
            "govt jobs only", "limited scope", "over supply"
        ],
        "base_score": 20,
        "bump": 10,
    },
    "time": {
        "keywords": [
            "years", "long time", "slow", "5 years", "10 years", "decade",
            "delay", "late", "old age", "age limit", "over age", "already late"
        ],
        "base_score": 15,
        "bump": 8,
    },
}

ALTERNATIVES = {
    "dropout": [
        "Take a gap semester with a clear plan instead of dropping out",
        "Start building your startup on weekends while still in college",
        "Apply to college entrepreneurship cells or startup incubators"
    ],
    "abroad": [
        "Explore IITs/NITs for M.Tech (equal quality at 1/10th the cost)",
        "Apply for fully-funded scholarships (DAAD, Erasmus, MEXT)",
        "Work for 1–2 years in India to save for abroad expenses"
    ],
    "startup": [
        "Validate the idea with 10 paying customers before full commitment",
        "Apply to Y Combinator, Antler, or Startup India for funding",
        "Keep a 12-month savings runway before quitting a stable job"
    ],
    "government": [
        "Prepare for government exams alongside college to hedge",
        "Focus on top-tier exams (UPSC/State PSC) rather than SSC for better ROI",
        "Give yourself a 2-attempt limit, then pivot to private sector"
    ],
    "default": [
        "Research the field deeply before committing (talk to 5 people in the domain)",
        "Start with a smaller commitment to test the path",
        "Identify a mentor in your chosen field",
        "Build savings before taking high-risk paths",
    ]
}


class RiskEngine:
    """Detects and scores multiple risk types in career/life decisions."""

    def assess_risk(self, option: str, user_profile: str = None) -> RiskResponse:
        """Assess risk for a given career option/plan."""
        combined_text = f"{option} {user_profile or ''}".lower()
        risks = []
        total_score = 0.0

        for risk_type, config in RISK_SIGNALS.items():
            matched_signals = [kw for kw in config["keywords"] if kw in combined_text]
            if matched_signals:
                score = min(100.0, config["base_score"] + config["bump"] * len(matched_signals))
            else:
                score = config["base_score"]

            # Slightly randomize to avoid all identical signals for demo realism
            score = min(100.0, score)

            label = get_risk_label(score)
            description = self._describe_risk(risk_type, matched_signals)
            mitigation = self._mitigate_risk(risk_type, option)

            risks.append(RiskItem(
                risk_type=risk_type.replace("_", " ").title(),
                level=label,
                score=round(score, 1),
                description=description,
                mitigation=mitigation,
            ))
            total_score += score

        overall_score = round(total_score / len(risks), 1)
        overall_label = get_risk_label(overall_score)
        alternatives = self._get_alternatives(option)
        recommendation = self._generate_recommendation(overall_label, option)

        return RiskResponse(
            option=option,
            overall_risk=overall_label,
            overall_score=overall_score,
            risks=risks,
            safer_alternatives=alternatives,
            recommendation=recommendation,
        )

    def _describe_risk(self, risk_type: str, signals: list[str]) -> str:
        descriptions = {
            "financial": f"Financial risks detected. Signals: {', '.join(signals[:3]) if signals else 'General financial uncertainty'}. This path may impact income stability.",
            "skill_gap": f"Skill gap risks detected. Signals: {', '.join(signals[:3]) if signals else 'Possible mismatch between current and required skills'}. Upskilling may be required.",
            "market": f"Market risks detected. Signals: {', '.join(signals[:3]) if signals else 'Market conditions uncertain'}. External demand may limit opportunities.",
            "time": f"Time-based risks detected. Signals: {', '.join(signals[:3]) if signals else 'Long preparation time required'}. This path requires significant time investment.",
        }
        return descriptions.get(risk_type, "Risk identified in this dimension.")

    def _mitigate_risk(self, risk_type: str, option: str) -> str:
        mitigations = {
            "financial": "Maintain a 6-month emergency fund before committing. Explore scholarships, fellowships, and part-time income sources.",
            "skill_gap": "Enroll in a structured course (Coursera, NPTEL) and build 2–3 projects before applying. Set a 6-month upskilling target.",
            "market": "Research the actual job market on Naukri/LinkedIn. Speak to 5 professionals in the field. Identify high-demand sub-niches.",
            "time": "Set clear milestones with deadlines. Define a 'pivot point' — if goal isn't achieved by X date, switch to alternative plan B.",
        }
        return mitigations.get(risk_type, "Research thoroughly, talk to people in the field, and create a contingency plan.")

    def _get_alternatives(self, option: str) -> list[str]:
        option_lower = option.lower()
        for keyword, alts in ALTERNATIVES.items():
            if keyword in option_lower:
                return alts
        return ALTERNATIVES["default"]

    def _generate_recommendation(self, risk_level: str, option: str) -> str:
        if risk_level == "High":
            return (
                f"⚠️ High risk detected. '{option[:60]}...' carries significant risks. "
                "We recommend validating with a smaller commitment first, building a financial runway, "
                "and having a clear Plan B before fully committing."
            )
        elif risk_level == "Medium":
            return (
                f"🟡 Moderate risk. '{option[:60]}...' is viable but requires careful planning. "
                "Address skill gaps, ensure financial stability, and set clear milestones with timelines."
            )
        else:
            return (
                f"✅ Low risk path. '{option[:60]}...' appears well-considered. "
                "Ensure you have a clear execution plan and stay consistent with your timeline."
            )


_risk_instance = None


def get_risk_engine() -> RiskEngine:
    global _risk_instance
    if _risk_instance is None:
        _risk_instance = RiskEngine()
    return _risk_instance
