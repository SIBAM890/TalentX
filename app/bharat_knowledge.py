"""
TalentX – Bharat Knowledge Layer
India-specific scholarship, career outlook, and college data.
"""
import logging
from app.config import SCHOLARSHIP_DATA_PATH, CAREER_PATHS_PATH
from app.utils import load_json
from app.models import ScholarshipItem, ScholarshipResponse, CareerOutlookResponse

logger = logging.getLogger("talentx.bharat")

_scholarship_data: dict = {}
_career_paths: dict = {}

STATE_ALIASES = {
    "od": "odisha", "orrisa": "odisha", "odisha": "odisha",
    "mh": "maharashtra", "mumbai": "maharashtra", "pune": "maharashtra",
    "ka": "karnataka", "bengaluru": "karnataka", "bangalore": "karnataka",
    "tn": "tamilnadu", "chennai": "tamilnadu", "tamil": "tamilnadu",
    "ts": "telangana", "hyderabad": "telangana",
    "ap": "andhra_pradesh", "andhra": "andhra_pradesh",
    "wb": "west_bengal", "kolkata": "west_bengal", "bengal": "west_bengal",
    "rj": "rajasthan", "jaipur": "rajasthan",
    "up": "uttar_pradesh", "lucknow": "uttar_pradesh",
    "br": "bihar", "patna": "bihar",
    "gj": "gujarat", "ahmedabad": "gujarat",
    "kl": "kerala", "kochi": "kerala", "trivandrum": "kerala",
}


def _get_scholarship_data() -> dict:
    global _scholarship_data
    if not _scholarship_data:
        _scholarship_data = load_json(SCHOLARSHIP_DATA_PATH)
    return _scholarship_data


def _get_career_paths() -> dict:
    global _career_paths
    if not _career_paths:
        _career_paths = load_json(CAREER_PATHS_PATH)
    return _career_paths


def _normalize_state(state: str) -> str:
    state_lower = state.lower().strip()
    for alias, normalized in STATE_ALIASES.items():
        if alias in state_lower:
            return normalized
    return state_lower


def _parse_scholarship(raw: dict) -> ScholarshipItem:
    return ScholarshipItem(
        name=raw.get("name", ""),
        authority=raw.get("authority", ""),
        amount=raw.get("amount", ""),
        eligibility=raw.get("eligibility", ""),
        income_limit=raw.get("income_limit", ""),
        apply_at=raw.get("apply_at", ""),
        level=raw.get("level", []),
    )


class BharatKnowledge:
    """India-specific knowledge: scholarships, career outlook, state data."""

    def get_scholarships(
        self,
        state: str = "all",
        category: str = "all",
        education_level: str = "all",
    ) -> ScholarshipResponse:
        """Get scholarships filtered by state, category, and education level."""
        data = _get_scholarship_data()
        norm_state = _normalize_state(state)

        # Central schemes (always included)
        central = [_parse_scholarship(s) for s in data.get("central_schemes", [])]

        # State schemes
        state_schemes_raw = data.get("state_schemes", {})
        state_result = []
        if norm_state == "all":
            for schemes in state_schemes_raw.values():
                state_result.extend([_parse_scholarship(s) for s in schemes])
        else:
            matched_state = None
            for key in state_schemes_raw:
                if key in norm_state or norm_state in key:
                    matched_state = key
                    break
            if matched_state:
                state_result = [_parse_scholarship(s) for s in state_schemes_raw[matched_state]]

        # Private scholarships
        private = [_parse_scholarship(s) for s in data.get("private_scholarships", [])]

        # Filter by education level
        def level_filter(item: ScholarshipItem) -> bool:
            if education_level == "all":
                return True
            return any(education_level.lower() in lvl.lower() for lvl in item.level)

        central = list(filter(level_filter, central))
        state_result = list(filter(level_filter, state_result))
        private = list(filter(level_filter, private))

        total = len(central) + len(state_result) + len(private)
        recommendation = self._scholarship_recommendation(central + state_result + private)

        return ScholarshipResponse(
            state=state,
            category=category,
            total_found=total,
            central_schemes=central[:5],
            state_schemes=state_result[:5],
            private_scholarships=private[:4],
            recommendation=recommendation,
        )

    def get_career_outlook(self, domain: str) -> CareerOutlookResponse:
        """Get India-specific career outlook for a domain."""
        paths = _get_career_paths()

        # Find best matching path
        domain_lower = domain.lower()
        matched_key = None
        for key in paths:
            if domain_lower in key or any(
                word in key for word in domain_lower.split()
            ):
                matched_key = key
                break

        if not matched_key:
            # Try reverse: key in domain
            for key in paths:
                if key in domain_lower:
                    matched_key = key
                    break

        if not matched_key:
            return self._generic_outlook(domain)

        path = paths[matched_key]
        key_skills = path.get("skills_required", [])[:6] + path.get("skills_preferred", [])[:3]

        return CareerOutlookResponse(
            domain=domain,
            title=path.get("title", domain),
            demand=path.get("demand", "High"),
            avg_salary=path.get("avg_salary", "₹8–18 LPA"),
            entry_salary=path.get("entry_salary", "₹5–8 LPA"),
            senior_salary=path.get("senior_salary", "₹20–40 LPA"),
            growth_potential=path.get("growth_potential", "High"),
            top_companies=path.get("top_companies", ["TCS", "Infosys", "Wipro", "Amazon", "Google"])[:6],
            key_skills=key_skills[:8],
            job_market_note=self._market_note(matched_key),
        )

    def _generic_outlook(self, domain: str) -> CareerOutlookResponse:
        return CareerOutlookResponse(
            domain=domain,
            title=domain.replace("_", " ").title(),
            demand="Medium",
            avg_salary="₹6–15 LPA",
            entry_salary="₹4–7 LPA",
            senior_salary="₹15–30 LPA",
            growth_potential="Medium-High",
            top_companies=["TCS", "Infosys", "Wipro", "Accenture", "Cognizant"],
            key_skills=["Communication", "Problem Solving", "Domain Knowledge", "Python or Java", "SQL"],
            job_market_note="India's digital economy is growing. Upskilling in AI and cloud will enhance growth opportunities.",
        )

    def _scholarship_recommendation(self, all_schemes: list[ScholarshipItem]) -> str:
        if not all_schemes:
            return "Check the National Scholarship Portal (scholarships.gov.in) for all available schemes."
        top = all_schemes[0]
        return (
            f"Top recommendation: **{top.name}** by {top.authority}. "
            f"Amount: {top.amount}. Apply at: {top.apply_at}. "
            f"Also explore the National Scholarship Portal (https://scholarships.gov.in) for more."
        )

    def _market_note(self, path_key: str) -> str:
        notes = {
            "ai_ml_engineer": "India's AI market will reach $7.8 billion by 2025 (NASSCOM). AI/ML engineers are among the most sought-after professionals.",
            "software_developer": "India has 5.8 million software developers. Top product companies pay 2–3x more than services firms.",
            "data_analyst": "Data analytics jobs in India grew 45% YoY. BI and SQL skills remain highly valuable across all industries.",
            "cybersecurity_analyst": "India faces 1.7 million cybersecurity professional shortage. This is a golden opportunity for security professionals.",
            "devops_engineer": "DevOps adoption in India is at 62% (Puppet report). Demand far exceeds supply, especially for cloud-native skills.",
            "product_manager": "Product management is one of the fastest-growing roles. IIM/IIT grads command ₹30–60 LPA at top startups.",
        }
        return notes.get(path_key, "This field is growing in India. Build a strong portfolio and network actively on LinkedIn.")

    def list_states(self) -> list[str]:
        data = _get_scholarship_data()
        return list(data.get("state_schemes", {}).keys())


_bharat_instance = None


def get_bharat_knowledge() -> BharatKnowledge:
    global _bharat_instance
    if _bharat_instance is None:
        _bharat_instance = BharatKnowledge()
    return _bharat_instance
