"""
TalentX – Pydantic Models (Request & Response Schemas)
"""
from typing import Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# CANDIDATE MODELS
# ─────────────────────────────────────────────

class CandidateDecisionRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Student's career decision query")
    user_background: Optional[str] = Field(None, description="Brief background (degree, skills, etc.)")
    location: Optional[str] = Field(None, description="State/city in India")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "I am a BTech CSE student confused between GATE, placements, and higher studies abroad",
                "user_background": "3rd year BTech CSE, CGPA 8.0, know Python and ML basics",
                "location": "Odisha"
            }
        }
    }


class TimelineMilestone(BaseModel):
    year: int
    milestone: str
    action: str
    status: str = "pending"


class DecisionOption(BaseModel):
    name: str
    description: str
    cost: str
    cost_score: float
    time_required: str
    risk_level: str
    risk_score: float
    growth_potential: str
    growth_score: float
    expected_salary: str
    confidence: float
    timeline: list[TimelineMilestone]
    pros: list[str]
    cons: list[str]


class CandidateDecisionResponse(BaseModel):
    query: str
    options: list[DecisionOption]
    recommendation: str
    overall_confidence: float
    bharat_context: Optional[str] = None


class TimelineRequest(BaseModel):
    career_path: str = Field(..., description="Career path key (e.g., 'ai_ml_engineer')")
    current_skills: Optional[list[str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "career_path": "ai_ml_engineer",
                "current_skills": ["Python", "SQL"]
            }
        }
    }


class TimelineResponse(BaseModel):
    career_path: str
    title: str
    milestones: list[TimelineMilestone]
    total_duration: str
    expected_salary: str


# ─────────────────────────────────────────────
# RISK MODELS
# ─────────────────────────────────────────────

class RiskRequest(BaseModel):
    option: str = Field(..., description="Career option or plan to assess")
    user_profile: Optional[str] = Field(None, description="Current student profile")

    model_config = {
        "json_schema_extra": {
            "example": {
                "option": "I want to drop out of college and start a startup",
                "user_profile": "2nd year BTech, no savings, family income ₹5 lakh/year"
            }
        }
    }


class RiskItem(BaseModel):
    risk_type: str
    level: str
    score: float
    description: str
    mitigation: str


class RiskResponse(BaseModel):
    option: str
    overall_risk: str
    overall_score: float
    risks: list[RiskItem]
    safer_alternatives: list[str]
    recommendation: str


# ─────────────────────────────────────────────
# RECRUITER MODELS
# ─────────────────────────────────────────────

class ResumeData(BaseModel):
    name: str
    content: str


class RecruiterRankRequest(BaseModel):
    jd_text: str = Field(..., min_length=20, description="Job description text")
    resumes: list[ResumeData] = Field(..., min_length=1, description="List of resumes with name and content")

    model_config = {
        "json_schema_extra": {
            "example": {
                "jd_text": "We need a Data Scientist with 3+ years Python, ML, and NLP experience...",
                "resumes": [
                    {"name": "Rahul Sharma", "content": "Senior Data Scientist with 5 years..."},
                    {"name": "Priya Mehta", "content": "Data Scientist with 3 years..."}
                ]
            }
        }
    }


class CandidateScore(BaseModel):
    name: str
    rank: int
    total_score: float
    skill_match: float
    semantic_similarity: float
    experience_fit: float
    education_fit: float
    keyword_coverage: float
    years_experience: float
    education_level: str
    matched_skills: list[str]
    missing_skills: list[str]
    summary: str


class RecruiterRankResponse(BaseModel):
    jd_summary: str
    total_candidates: int
    ranked_candidates: list[CandidateScore]
    top_pick: str
    evaluation_note: str


# ─────────────────────────────────────────────
# FAMILY DECISION MODELS
# ─────────────────────────────────────────────

class FamilyDecisionRequest(BaseModel):
    student_view: str = Field(..., description="Student's perspective and preference")
    parent_view: str = Field(..., description="Parent's perspective and concerns")
    student_name: Optional[str] = Field(None, description="Student name (optional)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "student_view": "I want to pursue AI research and go abroad for MS",
                "parent_view": "We want you to get a stable job near home and support family",
                "student_name": "Rohan"
            }
        }
    }


class FamilyDecisionResponse(BaseModel):
    student_goal: str
    parent_concern: str
    balanced_recommendation: str
    compromise_path: str
    student_satisfaction: float
    parent_satisfaction: float
    compromise_score: float
    action_steps: list[str]
    timeline: str
    key_insight: str


# ─────────────────────────────────────────────
# BHARAT KNOWLEDGE MODELS
# ─────────────────────────────────────────────

class ScholarshipItem(BaseModel):
    name: str
    authority: str
    amount: str
    eligibility: str
    income_limit: str
    apply_at: str
    level: list[str]


class ScholarshipResponse(BaseModel):
    state: str
    category: str
    total_found: int
    central_schemes: list[ScholarshipItem]
    state_schemes: list[ScholarshipItem]
    private_scholarships: list[ScholarshipItem]
    recommendation: str


class CareerOutlookResponse(BaseModel):
    domain: str
    title: str
    demand: str
    avg_salary: str
    entry_salary: str
    senior_salary: str
    growth_potential: str
    top_companies: list[str]
    key_skills: list[str]
    job_market_note: str


# ─────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: bool
    message: str
