"""
TalentX – Decision Engine (DishaSetu Mode)
Career decision simulation and comparison for Indian students.
"""
import re
import logging
from app.config import CAREER_PATHS_PATH
from app.llm_client import get_llm_client
from app.utils import load_json
from app.models import (
    DecisionOption, TimelineMilestone, CandidateDecisionResponse
)

logger = logging.getLogger("talentx.decision")

# Query keyword → career option mapping
OPTION_KEYWORDS = {
    "gate": {
        "name": "GATE / M.Tech in India",
        "careers": ["mtech_msc", "government_services"],
        "description": "Post-graduate technical degree via GATE exam. Opens doors to PSUs, IIT/NIT M.Tech, and R&D roles.",
        "cost": "Low (₹30,000–3 lakh/year)",
        "cost_score": 85,
        "time_required": "2 years + 1 year GATE prep",
        "risk_level": "Low",
        "risk_score": 25,
        "growth_potential": "Medium-High",
        "growth_score": 70,
        "expected_salary": "₹8–20 LPA",
        "pros": ["Low cost", "Prestigious IITs/NITs", "PSU eligibility (₹10–20 LPA)", "Research opportunities"],
        "cons": ["Competitive exam", "3 years time investment", "Limited seats"],
    },
    "placement": {
        "name": "Campus Placement / Job",
        "careers": ["software_developer", "data_analyst"],
        "description": "Direct industry entry via college placements or job applications. Fastest path to income.",
        "cost": "Low (interview prep only)",
        "cost_score": 95,
        "time_required": "6 months–1 year",
        "risk_level": "Low",
        "risk_score": 20,
        "growth_potential": "High",
        "growth_score": 75,
        "expected_salary": "₹4–15 LPA",
        "pros": ["Immediate income", "Fast career start", "Industry exposure", "Low upfront cost"],
        "cons": ["Entry-level salary", "Requires strong DSA/skills", "Competition from peers"],
    },
    "abroad": {
        "name": "MS / Higher Studies Abroad",
        "careers": ["higher_studies_abroad"],
        "description": "Masters program in USA/Canada/Germany. Best for research and global career growth.",
        "cost": "Very High (₹40–80 lakh total)",
        "cost_score": 25,
        "time_required": "2 years + 1 year GRE prep",
        "risk_level": "Medium",
        "risk_score": 55,
        "growth_potential": "Very High",
        "growth_score": 92,
        "expected_salary": "₹20–60 LPA (India return) / USD salary abroad",
        "pros": ["Global exposure", "High salary", "Research opportunities", "Visa pathway (H1B, PR)"],
        "cons": ["Very expensive", "Visa uncertainty", "Homesickness", "Competitive admissions"],
    },
    "startup": {
        "name": "Build a Startup",
        "careers": ["startup_founder"],
        "description": "Entrepreneurship path — solve a real problem and build a company.",
        "cost": "Medium (self-funded initially)",
        "cost_score": 50,
        "time_required": "3–7 years to meaningful outcome",
        "risk_level": "High",
        "risk_score": 80,
        "growth_potential": "Extreme",
        "growth_score": 98,
        "expected_salary": "₹0 to unlimited (equity-based)",
        "pros": ["Unlimited upside", "Build something impactful", "Be your own boss", "India startup ecosystem growing"],
        "cons": ["90% failure rate", "No stable income", "High stress", "Family pressure in India"],
    },
    "mba": {
        "name": "MBA (IIM / Top B-School)",
        "careers": ["mba"],
        "description": "Management post-graduation. Opens doors to consulting, product management, and leadership roles.",
        "cost": "High (₹20–25 lakh)",
        "cost_score": 35,
        "time_required": "2 years + 1–2 years CAT prep",
        "risk_level": "Medium",
        "risk_score": 40,
        "growth_potential": "Very High",
        "growth_score": 88,
        "expected_salary": "₹15–50 LPA (IIM A/B/C)",
        "pros": ["High salary", "Leadership roles", "Network", "IIM brand value"],
        "cons": ["Very expensive", "Tough admission (99+ CAT percentile)", "2 years + prep time"],
    },
    "upsc": {
        "name": "UPSC / Government Services",
        "careers": ["government_services"],
        "description": "Indian Civil Services — IAS/IPS/IFS. Highest job security, prestige, and societal impact.",
        "cost": "Low-Medium (coaching optional)",
        "cost_score": 70,
        "time_required": "2–5 years preparation",
        "risk_level": "Medium",
        "risk_score": 50,
        "growth_potential": "Medium (high stability)",
        "growth_score": 65,
        "expected_salary": "₹6–25 LPA + perks",
        "pros": ["Extreme job security", "Social impact", "Prestige", "Perks (housing, car, pension)"],
        "cons": ["Very long prep time", "High competition", "Limited attempts", "Opportunity cost"],
    },
    "data_science": {
        "name": "Data Science / AI Career",
        "careers": ["ai_ml_engineer", "data_analyst"],
        "description": "Specialization in data science, machine learning, or AI. One of the hottest career paths globally.",
        "cost": "Low-Medium (courses + projects)",
        "cost_score": 75,
        "time_required": "1–2 years",
        "risk_level": "Low",
        "risk_score": 22,
        "growth_potential": "Very High",
        "growth_score": 95,
        "expected_salary": "₹6–25 LPA",
        "pros": ["Extremely high demand", "Global opportunities", "Work from home", "Fast salary growth"],
        "cons": ["Requires strong math foundation", "Continuous learning needed", "Competition increasing"],
    },
    "freelancing": {
        "name": "Freelancing / Independent Consulting",
        "careers": ["freelancer"],
        "description": "Work independently on projects for clients via platforms like Upwork/Toptal or directly.",
        "cost": "Very Low",
        "cost_score": 95,
        "time_required": "3–6 months to first income",
        "risk_level": "Medium",
        "risk_score": 45,
        "growth_potential": "High",
        "growth_score": 80,
        "expected_salary": "₹3–30 LPA (highly variable)",
        "pros": ["Flexible hours", "Work from anywhere", "No boss", "Skill-based income"],
        "cons": ["Income instability", "No job benefits", "Marketing required", "Lonely work"],
    },
}

# Generic timeline when career path is unknown
GENERIC_TIMELINE = [
    TimelineMilestone(year=1, milestone="Build core skills and foundation", action="Take structured courses, read books", status="pending"),
    TimelineMilestone(year=2, milestone="Gain hands-on experience", action="Internship, projects, freelancing", status="pending"),
    TimelineMilestone(year=3, milestone="Land first major role or goal", action="Apply actively, network, interview", status="pending"),
    TimelineMilestone(year=5, milestone="Specialization and leadership", action="Certifications, mentoring, advanced skills", status="pending"),
]


def _detect_options(query: str) -> list[str]:
    """Detect which career options are mentioned in the query."""
    query_lower = query.lower()
    found = []

    keyword_map = {
        "gate": ["gate", "m.tech", "mtech", "iit", "nit", "psu"],
        "placement": ["placement", "job", "employ", "campus", "hire", "work"],
        "abroad": ["abroad", "foreign", "usa", "ms", "masters", "gre", "us college", "canada", "germany", "uk", "australia"],
        "startup": ["startup", "entrepreneur", "company", "business", "found", "venture"],
        "mba": ["mba", "management", "cat exam", "iim", "business school", "b-school"],
        "upsc": ["upsc", "ias", "ips", "civil service", "government exam", "ssc", "state psc"],
        "data_science": ["data science", "machine learning", "ai", "artificial intelligence", "ml engineer", "data scientist"],
        "freelancing": ["freelanc", "independent", "consulting", "upwork", "fiverr", "own client"],
    }
    for option_key, keywords in keyword_map.items():
        if any(kw in query_lower for kw in keywords):
            found.append(option_key)

    # If nothing found or very generic query, suggest top 3 popular options
    if len(found) < 2:
        if not found:
            found = ["placement", "data_science", "gate"]
        elif len(found) == 1:
            found += ["placement", "data_science"] if found[0] not in ["placement", "data_science"] else ["gate", "abroad"]

    return found[:4]  # Max 4 options


def _build_timeline_from_path(careers: list[str]) -> list[TimelineMilestone]:
    """Load milestones from career path data."""
    paths = load_json(CAREER_PATHS_PATH)
    for career_key in careers:
        if career_key in paths:
            raw = paths[career_key].get("yearly_milestones", [])
            return [
                TimelineMilestone(year=m["year"], milestone=m["milestone"], action=m["action"], status="pending")
                for m in raw
            ]
    return GENERIC_TIMELINE


def _calculate_confidence(option_key: str, query: str) -> float:
    """Estimate confidence score based on how clearly the option fits the query."""
    query_lower = query.lower()
    option = OPTION_KEYWORDS.get(option_key, {})
    base = 60.0
    # Boost if keywords match strongly
    if option_key in query_lower:
        base += 15
    # Positive signals
    positive = ["confused", "should i", "which is better", "help", "guide", "career", "future"]
    for word in positive:
        if word in query_lower:
            base += 2
    return min(95.0, round(base, 1))


class DecisionEngine:
    """DishaSetu Mode – career decision simulator for Indian students."""

    def simulate_options(self, request) -> CandidateDecisionResponse:
        """Generate a comparison of career options from a student query."""
        query = request.query
        detected = _detect_options(query)

        options_out = []
        for key in detected:
            if key not in OPTION_KEYWORDS:
                continue
            data = OPTION_KEYWORDS[key]
            timeline = _build_timeline_from_path(data.get("careers", []))
            confidence = _calculate_confidence(key, query)

            options_out.append(DecisionOption(
                name=data["name"],
                description=data["description"],
                cost=data["cost"],
                cost_score=data["cost_score"],
                time_required=data["time_required"],
                risk_level=data["risk_level"],
                risk_score=data["risk_score"],
                growth_potential=data["growth_potential"],
                growth_score=data["growth_score"],
                expected_salary=data["expected_salary"],
                confidence=confidence,
                timeline=timeline,
                pros=data["pros"],
                cons=data["cons"],
            ))

        # Sort by overall desirability (growth - risk + cost_score) / 3
        options_out.sort(
            key=lambda o: (o.growth_score + o.cost_score - o.risk_score) / 3,
            reverse=True
        )

        top = options_out[0] if options_out else None
        recommendation = (
            f"Based on your query, **{top.name}** appears to be the best starting point "
            f"with {top.growth_potential} growth potential and {top.risk_level} risk. "
            f"Expected salary: {top.expected_salary}."
        ) if top else "Please provide more details about your situation for a personalized recommendation."
        recommendation = self._enhance_recommendation(query, options_out, recommendation)

        bharat_context = self._bharat_context(request)

        return CandidateDecisionResponse(
            query=query,
            options=options_out,
            recommendation=recommendation,
            overall_confidence=options_out[0].confidence if options_out else 60.0,
            bharat_context=bharat_context,
        )

    def _bharat_context(self, request) -> str:
        """Add India-specific context based on user location."""
        location = (request.location or "").lower()
        context_map = {
            "odisha": "Odisha has the PRERANA and Medhabruti scholarships. Bhubaneswar is a growing IT hub.",
            "bihar": "Bihar's Mukhyamantri Kanya Utthan Yojana offers ₹50,000 for girl graduates. Patna is emerging in EdTech.",
            "kerala": "Kerala has one of India's highest literacy rates and growing IT sector in Kochi (Infopark).",
            "maharashtra": "Mumbai/Pune are tier-1 job markets. Maharashtra has strong startup ecosystem (T-Hub adjacent).",
            "bengaluru": "Bengaluru is India's Silicon Valley — highest density of tech jobs and startups.",
            "hyderabad": "Hyderabad's HITEC City is a top 3 tech hub. Telangana ePass covers full college fees.",
        }
        for key, ctx in context_map.items():
            if key in location:
                return ctx
        return "India's tech sector is growing rapidly with 1,000+ unicorns by 2030 expected. Act now to capitalize."

    def _enhance_recommendation(
        self,
        query: str,
        options: list[DecisionOption],
        fallback: str,
    ) -> str:
        """Use OpenRouter to write a sharper recommendation when configured."""
        if not options:
            return fallback

        option_summary = "\n".join(
            f"- {option.name}: risk={option.risk_level}, growth={option.growth_potential}, "
            f"salary={option.expected_salary}, confidence={option.confidence:.0f}%"
            for option in options[:4]
        )
        prompt = (
            "Student query:\n"
            f"{query}\n\n"
            "Options detected:\n"
            f"{option_summary}\n\n"
            "Write a concise India-specific recommendation in 3-4 sentences. "
            "Name the best first step, one key risk, and one practical next action. "
            "Do not mention that you are an AI model."
        )
        enhanced = get_llm_client().chat(
            "You are TalentX, a practical career decision assistant for Indian students.",
            prompt,
            max_tokens=220,
        )
        return enhanced or fallback


_decision_instance = None


def get_decision_engine() -> DecisionEngine:
    global _decision_instance
    if _decision_instance is None:
        _decision_instance = DecisionEngine()
    return _decision_instance
