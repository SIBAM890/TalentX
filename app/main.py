"""
TalentX – FastAPI Main Application
All API endpoints for Candidate, Recruiter, Family, and Bharat layers.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from app.models import (
    CandidateDecisionRequest, CandidateDecisionResponse,
    TimelineRequest, TimelineResponse,
    RiskRequest, RiskResponse,
    RecruiterRankRequest, RecruiterRankResponse,
    FamilyDecisionRequest, FamilyDecisionResponse,
    ScholarshipResponse, CareerOutlookResponse,
    HealthResponse,
)
from app.decision_engine import get_decision_engine
from app.timeline_engine import get_timeline_engine
from app.risk_engine import get_risk_engine
from app.ranking_engine import get_ranking_engine
from app.family_engine import get_family_engine
from app.bharat_knowledge import get_bharat_knowledge
from app.resource_hub import get_resource_hub

logger = logging.getLogger("talentx.api")

# ─── App Initialization ───────────────────────────────────────────────────────

app = FastAPI(
    title="TalentX API",
    description=(
        "**TalentX** – The X Factor in Hiring & Life Decisions.\n\n"
        "Dual-sided AI platform for:\n"
        "- **DishaSetu Mode**: Career decision simulation for Indian students\n"
        "- **TalentX Mode**: Intelligent candidate ranking for recruiters\n\n"
        "Built for the **India Runs Hackathon by Redrob AI** | Track 1: Data & AI Challenge"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request Timing Middleware ─────────────────────────────────────────────────

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(duration)
    return response


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and model loading status."""
    try:
        # Light check — try importing models
        from app.nlp_pipeline import _get_sbert
        model = _get_sbert()
        models_loaded = model is not None
    except Exception:
        models_loaded = False

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        models_loaded=models_loaded,
        message="TalentX API is running. Use /docs for full API documentation.",
    )


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "🚀 TalentX API – The X Factor in Hiring & Life Decisions",
        "docs": "/docs",
        "health": "/api/health",
        "version": "1.0.0",
        "modes": {
            "candidate": "/api/candidate/*",
            "recruiter": "/api/recruiter/*",
            "family": "/api/family/*",
            "bharat": "/api/bharat/*",
        }
    }


# ─── Candidate Endpoints ───────────────────────────────────────────────────────

@app.post(
    "/api/candidate/decide",
    response_model=CandidateDecisionResponse,
    tags=["Candidate – DishaSetu Mode"],
    summary="Simulate career options for a student query",
)
async def candidate_decide(request: CandidateDecisionRequest):
    """
    **DishaSetu Mode**: Simulate and compare career paths for a student.

    Provide a natural language query like:
    - "I'm a BTech CSE student confused between GATE, placements, and higher studies abroad"
    - "Should I do MBA or data science after my BCA?"
    - "I want to start a startup vs get a job — help me decide"

    Returns a comparison of options with cost, risk, growth, timeline, and confidence scores.
    """
    try:
        engine = get_decision_engine()
        result = engine.simulate_options(request)
        return result
    except Exception as e:
        logger.error(f"Decision engine error: {e}")
        raise HTTPException(status_code=500, detail=f"Decision engine error: {str(e)}")


@app.post(
    "/api/candidate/timeline",
    response_model=TimelineResponse,
    tags=["Candidate – DishaSetu Mode"],
    summary="Get year-by-year career timeline",
)
async def candidate_timeline(request: TimelineRequest):
    """
    Get a detailed year-by-year roadmap for a specific career path.

    Available paths: ai_ml_engineer, software_developer, data_analyst,
    product_manager, cybersecurity_analyst, devops_engineer, ux_designer,
    data_engineer, startup_founder, mba, higher_studies_abroad, etc.
    """
    try:
        engine = get_timeline_engine()
        return engine.get_timeline(request.career_path, request.current_skills)
    except Exception as e:
        logger.error(f"Timeline engine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/candidate/careers",
    tags=["Candidate – DishaSetu Mode"],
    summary="List all available career paths",
)
async def list_careers():
    """List all available career paths with key metadata."""
    try:
        engine = get_timeline_engine()
        return {"career_paths": engine.list_available_paths()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/api/candidate/risk",
    response_model=RiskResponse,
    tags=["Candidate – DishaSetu Mode"],
    summary="Assess risk for a career decision",
)
async def candidate_risk(request: RiskRequest):
    """
    Assess the risk of a career option or plan.

    Detects 4 risk types:
    - **Financial Risk**: Income instability, high costs
    - **Skill Gap Risk**: Missing required skills
    - **Market Risk**: Low demand or saturated market
    - **Time Risk**: Excessive time investment

    Returns risk scores with mitigation strategies and safer alternatives.
    """
    try:
        engine = get_risk_engine()
        return engine.assess_risk(request.option, request.user_profile)
    except Exception as e:
        logger.error(f"Risk engine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/candidate/resources/{career_key}",
    tags=["Candidate – DishaSetu Mode"],
    summary="Get learning resources for a career path",
)
async def get_resources(career_key: str):
    """Get curated courses, certifications, and communities for a career path."""
    try:
        hub = get_resource_hub()
        return hub.get_resources(career_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Recruiter Endpoints ───────────────────────────────────────────────────────

@app.post(
    "/api/recruiter/rank",
    response_model=RecruiterRankResponse,
    tags=["Recruiter – TalentX Mode"],
    summary="Rank candidates against a job description",
)
async def recruiter_rank(request: RecruiterRankRequest):
    """
    **TalentX Mode**: Intelligently rank candidates against a job description.

    Uses a 5-dimensional hybrid scoring system:
    - **Skill Match** (35%): Direct skill overlap between JD and resume
    - **Semantic Similarity** (25%): Sentence-BERT embedding cosine similarity
    - **Experience Fit** (20%): Years of experience vs. requirement
    - **Education Fit** (10%): Highest qualification scoring
    - **Keyword Coverage** (10%): JD keyword coverage in resume

    Returns a ranked list with transparent score breakdowns.
    """
    try:
        engine = get_ranking_engine()
        resume_dicts = [{"name": r.name, "content": r.content} for r in request.resumes]
        return engine.rank_candidates(request.jd_text, resume_dicts)
    except Exception as e:
        logger.error(f"Ranking engine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/recruiter/sample",
    tags=["Recruiter – TalentX Mode"],
    summary="Load sample JD and resumes for testing",
)
async def recruiter_sample():
    """Load the sample JD and all sample resumes for a demo ranking run."""
    import os
    from app.config import SAMPLE_JD_PATH, SAMPLE_RESUMES_DIR

    try:
        with open(SAMPLE_JD_PATH, "r", encoding="utf-8") as f:
            jd_text = f.read()

        resumes = []
        for fname in sorted(os.listdir(SAMPLE_RESUMES_DIR)):
            if fname.endswith(".txt"):
                with open(SAMPLE_RESUMES_DIR / fname, "r", encoding="utf-8") as f:
                    content = f.read()
                name = fname.replace(".txt", "").replace("_", " ").title()
                # Extract actual name from first line
                first_line = content.split("\n")[0].replace("RESUME –", "").strip()
                resumes.append({"name": first_line or name, "content": content})

        return {
            "jd_text": jd_text[:500] + "...",
            "resume_count": len(resumes),
            "resume_names": [r["name"] for r in resumes],
            "note": "Use POST /api/recruiter/rank with this data to see rankings."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Family Decision Endpoints ─────────────────────────────────────────────────

@app.post(
    "/api/family/decide",
    response_model=FamilyDecisionResponse,
    tags=["Family Mode"],
    summary="Balance student and parent perspectives",
)
async def family_decide(request: FamilyDecisionRequest):
    """
    **Family Mode**: Generate a balanced recommendation from student + parent perspectives.

    Takes two viewpoints and generates:
    - Balanced recommendation
    - Compromise career path
    - Student satisfaction score
    - Parent satisfaction score
    - Actionable steps for both sides
    - Key insight into the core tension

    Culturally designed for Indian family decision dynamics.
    """
    try:
        engine = get_family_engine()
        return engine.balance_views(request)
    except Exception as e:
        logger.error(f"Family engine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── Bharat Knowledge Endpoints ───────────────────────────────────────────────

@app.get(
    "/api/bharat/scholarships",
    response_model=ScholarshipResponse,
    tags=["Bharat Knowledge Layer"],
    summary="Find scholarships by state and category",
)
async def get_scholarships(
    state: str = "all",
    category: str = "all",
    level: str = "all",
):
    """
    Find India-specific scholarships.

    - **state**: State name (e.g., 'odisha', 'maharashtra', 'kerala', 'all')
    - **category**: SC/ST/OBC/minority/general/all
    - **level**: UG/PG/Ph.D/Diploma/all

    Returns central government, state, and private scholarships.
    """
    try:
        knowledge = get_bharat_knowledge()
        return knowledge.get_scholarships(state, category, level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/bharat/career-outlook/{domain}",
    response_model=CareerOutlookResponse,
    tags=["Bharat Knowledge Layer"],
    summary="Get career outlook for a domain in India",
)
async def career_outlook(domain: str):
    """
    Get India-specific career outlook for a domain.

    Examples: ai_ml_engineer, software_developer, data_analyst,
    cybersecurity, devops, product_manager
    """
    try:
        knowledge = get_bharat_knowledge()
        return knowledge.get_career_outlook(domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/bharat/states",
    tags=["Bharat Knowledge Layer"],
    summary="List states with scholarship data",
)
async def list_states():
    """List all Indian states that have scholarship data available."""
    knowledge = get_bharat_knowledge()
    return {"states": knowledge.list_states(), "note": "Use state name in /api/bharat/scholarships?state=<name>"}


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    from app.config import APP_HOST, APP_PORT, APP_DEBUG
    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=APP_DEBUG)
