# 🚀 TalentX – The X Factor in Hiring & Life Decisions

[![Built for India](https://img.shields.io/badge/Built%20for-India%20🇮🇳-orange?style=flat-square)](https://github.com)
[![Hackathon](https://img.shields.io/badge/India%20Runs-Redrob%20AI-blue?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal?style=flat-square)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red?style=flat-square)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> **"Not filters. Not advice. Intelligence."**

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Demo Walkthrough](#-demo-walkthrough)
- [Hackathon Submission](#-hackathon-submission)
- [Team](#-team)
- [License](#-license)

---

## 📖 Overview

**TalentX** is a dual-sided AI platform that serves two critical needs in India's education and hiring ecosystem:

### 🧭 Side A – DishaSetu Mode (Candidate)
An AI-powered career decision simulator that helps Indian students make informed choices by comparing multiple paths, assessing risks across 4 dimensions, and visualizing year-by-year timelines — with India-specific context including state scholarships and career outlook.

### 📊 Side B – TalentX Mode (Recruiter)
An intelligent candidate ranking system that moves beyond keyword filters to deliver semantically ranked shortlists using a 5-dimensional hybrid scoring model: **Skill Match (35%)** + **Semantic Similarity (25%)** + **Experience Fit (20%)** + **Education Fit (10%)** + **Keyword Coverage (10%)**.

Built for the **India Runs Hackathon by Redrob AI** (Track 1: The Data & AI Challenge, ₹50 Lakh+ Prize Pool).

---

## 🎯 Problem Statement

> *"Develop a robust, workable Proof of Concept that doesn't just filter, but intelligently ranks candidates."*

**The harsh reality of India's hiring & career landscape:**

| Problem | Impact |
|:---|:---|
| 98% of resumes rejected by ATS keyword filters | Hidden talent goes unnoticed |
| Recruiters spend only 6–7 seconds per resume | Context and nuance are lost |
| 70% of qualified candidates are "hidden gems" | Companies miss the best talent |
| Students make career decisions without data | Poor ROI on education investment |
| India-specific context (family dynamics, state schemes) ignored | Decisions made in a vacuum |

---

## 💡 Solution

**TalentX** bridges this gap with a single AI intelligence engine serving both sides:

### Side A – Candidate Decision Intelligence

| Feature | Description |
|:---|:---|
| **🔮 Decision Simulator** | Compare career options (BTech vs BCA vs BSc AI vs MBA) |
| **📅 Future Timeline** | Year-by-year roadmap for each path |
| **🛡️ Risk Detector** | Financial, Skill Gap, Market, and Time risk analysis |
| **👨‍👩‍👧 Family Decision Mode** | Balance student passion with parent stability |
| **🇮🇳 Bharat Knowledge Layer** | 50+ scholarships, career outlook, salary data |
| **📚 Resource Hub** | Courses, certifications, communities curated per path |

### Side B – Recruiter Ranking Intelligence

| Feature | Description |
|:---|:---|
| **🧠 Semantic Understanding** | Sentence-BERT embeddings (all-MiniLM-L6-v2) |
| **⚖️ Hybrid Ranking** | 5-dimension weighted scoring |
| **🔍 Skill Taxonomy** | 200+ skills across 10 categories |
| **📊 Score Explainability** | Transparent breakdown per candidate |
| **⚡ Fast Processing** | Batch embedding for 1000+ resumes |

---

## ✨ Key Features

### 🔮 1. Decision Simulator
> *"Should I do BTech, MBA, or UPSC?"*

AI compares options across:

| Dimension | How TalentX Scores It |
|:---|:---|
| Cost | Low / Medium / High with score (0–100) |
| Time Required | Months/Years with context |
| Risk Level | Low/Medium/High with 4-dimension breakdown |
| Growth Potential | With expected salary range (India LPA) |
| Confidence | How well the option fits the query |

### 📅 2. Future Timeline Generator
> *"If I choose Data Science, what does my next 5 years look like?"*

```
Year 1: Learn Python, Mathematics, ML basics → Complete Andrew Ng's ML course
Year 2: Build 3–5 projects, Kaggle competitions → Land internship
Year 3: First AI/ML role (₹6–10 LPA) → Network, apply to product companies
Year 4: Specialize in NLP/CV → AWS ML Specialty certification
Year 5: Senior ML Engineer (₹18–30 LPA) → Mentor, lead, publish
```

### 🛡️ 3. Risk Intelligence Engine
> *"I want to quit college and start a startup."*

TalentX detects 4 risk types:
- ⚠️ **Financial Risk** — Income instability, high costs, no savings
- ⚠️ **Skill Gap Risk** — Missing required technical/soft skills
- ⚠️ **Market Risk** — Low demand, saturated market, regulatory risk
- ⏱️ **Time Risk** — Excessive preparation time, age limits

With mitigation strategies and safer alternatives for each risk.

### 👨‍👩‍👧 4. Family Decision Mode
> *"Student wants MS abroad. Parents want stability in India."*

```
Student Satisfaction:  [████████░░] 8.2/10
Parent Satisfaction:   [███████░░░] 7.8/10
Compromise Score:      80%

Recommendation: M.Tech in India (IIT/NIT) + placement in top product company
```

### 🇮🇳 5. Bharat Knowledge Layer
> *"Which scholarships can I get in Odisha for my B.Tech?"*

- 🏛️ 8 Central Government schemes (NSP, Pragati, PM Yasasvi...)
- 🗺️ State schemes across 10+ states (Odisha, Maharashtra, Karnataka...)
- 🏢 6 Private scholarships (Reliance, Google, HDFC, ONGC...)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TALENTX INTELLIGENCE ENGINE                   │
│     Sentence-BERT Embeddings + Hybrid Scoring + Risk Analysis    │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┴───────────────────┐
          ▼                                       ▼
┌─────────────────────┐               ┌─────────────────────┐
│   CANDIDATE SIDE    │               │  RECRUITER SIDE     │
│   (DishaSetu Mode)  │               │   (TalentX Mode)    │
├─────────────────────┤               ├─────────────────────┤
│ Decision Simulator  │               │ Candidate Ranking   │
│ Future Timeline     │               │ Semantic Matching   │
│ Risk Detector       │               │ Skill Taxonomy      │
│ Family Decision     │               │ Experience Scoring  │
│ Bharat Knowledge    │               │ Education Scoring   │
│ Resource Hub        │               │ Explainable Scores  │
└─────────────────────┘               └─────────────────────┘
          │                                       │
          └───────────────────┬───────────────────┘
                              ▼
          ┌─────────────────────────────────────┐
          │            DATA LAYER               │
          │  skill_taxonomy.json (200+ skills)  │
          │  career_paths.json (15 paths)       │
          │  scholarship_data.json (50+ items)  │
          │  sample_resumes/ (10 resumes)       │
          └─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Backend** | Python 3.10+, FastAPI | REST API with async support |
| **NLP** | spaCy (en_core_web_sm) | Named Entity Recognition |
| **Embeddings** | Sentence-BERT (all-MiniLM-L6-v2) | Semantic similarity |
| **ML** | scikit-learn | TF-IDF fallback, scoring |
| **Frontend** | Streamlit + Plotly | Interactive UI with charts |
| **Data** | JSON, TXT | Skill taxonomy, careers, scholarships |
| **Deployment** | Docker, Render.com | Containerized production deploy |
| **Testing** | pytest | Unit and integration tests |

---

## 📁 Project Structure

```
talentx/
├── app/
│   ├── main.py              # FastAPI entry point (12 endpoints)
│   ├── models.py            # Pydantic v2 schemas
│   ├── config.py            # Configuration & constants
│   ├── nlp_pipeline.py      # SBERT + spaCy + TF-IDF fallback
│   ├── ranking_engine.py    # Hybrid 5-dim ranking
│   ├── decision_engine.py   # DishaSetu career simulation
│   ├── risk_engine.py       # 4-dimension risk analysis
│   ├── timeline_engine.py   # Year-by-year roadmap generator
│   ├── family_engine.py     # Family balance algorithm
│   ├── bharat_knowledge.py  # India scholarships & career data
│   ├── resource_hub.py      # Course/certification recommender
│   └── utils.py             # Helpers: text, scoring, extraction
├── data/
│   ├── skill_taxonomy.json  # 200+ skills, 10 categories
│   ├── career_paths.json    # 15 career paths with milestones
│   ├── scholarship_data.json # 50+ India scholarships
│   ├── sample_jd.txt        # Sample Data Scientist JD
│   └── sample_resumes/      # 10 sample candidate resumes
├── frontend/
│   ├── app.py               # Main Streamlit application
│   ├── components/
│   │   ├── candidate_tab.py # DishaSetu Mode UI
│   │   ├── recruiter_tab.py # TalentX Mode UI
│   │   └── family_tab.py    # Family Mode UI
│   └── assets/style.css     # Premium dark theme CSS
├── scripts/
│   ├── seed_data.py         # Data validation + smoke tests
│   ├── test_ranking.py      # CLI ranking demo
│   └── test_decision.py     # CLI decision + risk demo
├── tests/
│   ├── test_nlp.py          # NLP pipeline unit tests
│   ├── test_ranking.py      # Ranking engine unit tests
│   └── test_decision.py     # Decision/risk/family unit tests
├── docs/
│   ├── METHODOLOGY.md       # Technical deep-dive
│   ├── DEPLOYMENT.md        # Deployment guide
│   └── DEMO_SCRIPT.md       # 3-min demo script
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── .env.example
├── .gitignore
├── README.md
└── WORK_DONE.md
```

---

## 🚀 Quick Start

### Prerequisites
```bash
python --version   # Python 3.10+
git --version
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/talentx.git
cd talentx

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Copy environment config
cp .env.example .env
```

### Run Validation
```bash
# Validate all data files and run smoke tests
python scripts/seed_data.py
```

### Run CLI Demos
```bash
# Test decision engine
python scripts/test_decision.py

# Test ranking engine
python scripts/test_ranking.py
```

### Run Backend API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# API at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### Run Frontend
```bash
# React frontend
cd frontend-react
npm install
npm run dev
# UI at: http://localhost:5173
```

### Legacy Streamlit Frontend
```bash
streamlit run frontend/app.py
# UI at: http://localhost:8501
```

### Run Tests
```bash
pytest tests/ -v
```

### Docker
```bash
docker-compose up --build
# API: http://localhost:8000
# Frontend: http://localhost:8501
```

---

## 📡 API Documentation

Full Swagger docs available at `http://localhost:8000/docs`.

### Candidate Endpoints

#### POST `/api/candidate/decide`
Simulate and compare career options.

```json
{
  "query": "I'm a BTech student confused between GATE, placements, and MS abroad",
  "user_background": "3rd year BTech CSE, CGPA 8.0",
  "location": "Odisha"
}
```

**Response includes:** options comparison, risk levels, timelines, confidence scores, Bharat context.

#### POST `/api/candidate/timeline`
Get year-by-year career roadmap.

```json
{ "career_path": "ai_ml_engineer", "current_skills": ["Python", "SQL"] }
```

#### POST `/api/candidate/risk`
Assess 4-dimension risk for a decision.

```json
{
  "option": "I want to drop out and start a startup with no savings",
  "user_profile": "2nd year BTech, no savings, family income ₹5 LPA"
}
```

#### GET `/api/candidate/careers`
List all 15 available career paths.

---

### Recruiter Endpoints

#### POST `/api/recruiter/rank`
Rank candidates against a JD.

```json
{
  "jd_text": "Data Scientist with 3+ years Python, ML, NLP experience...",
  "resumes": [
    { "name": "Rahul Sharma", "content": "5 years Python ML TensorFlow..." },
    { "name": "Priya Mehta", "content": "3 years data science..." }
  ]
}
```

**Response:** Ranked list with `total_score`, `skill_match`, `semantic_similarity`, `experience_fit`, `education_fit`, `keyword_coverage`, matched/missing skills.

---

### Family Endpoints

#### POST `/api/family/decide`
Balance student and parent perspectives.

```json
{
  "student_view": "I want to pursue AI research abroad",
  "parent_view": "We need stability and proximity",
  "student_name": "Rohan"
}
```

---

### Bharat Endpoints

#### GET `/api/bharat/scholarships?state=odisha&level=UG`
Get India-specific scholarships.

#### GET `/api/bharat/career-outlook/{domain}`
Get career outlook for a domain in India.

---

## 🎬 Demo Walkthrough

### 3-Minute Demo Script

| Time | Section | What to Show |
|:---|:---|:---|
| 0:00–0:20 | Introduction | "TalentX is the AI that sees talent where others see noise. Two sides. One engine." |
| 0:20–1:20 | **DishaSetu Mode** | Enter query → Compare GATE vs Placement vs Abroad → Show risk scores → Show timeline → Family Mode |
| 1:20–2:20 | **TalentX Mode** | Load sample data → Run ranking → Show podium → Show radar charts → Export CSV |
| 2:20–2:45 | **Bharat Layer** | Show Odisha scholarships → Show career outlook for AI |
| 2:45–3:00 | Vision | "One AI engine. Two sides. Built for 1.4 billion Indians." |

---

## 🏆 Hackathon Submission

### Track
**Track 1: The Data & AI Challenge** – Intelligent Candidate Discovery  
**Event:** India Runs Hackathon by Redrob AI | ₹50 Lakh+ Prize Pool

### Why TalentX Will Win

1. **Dual-sided impact** — Serves both sides of the hiring equation
2. **India-first design** — Family dynamics, state scholarships, LPA salary data
3. **Explainable AI** — Every score is transparent and decomposed
4. **Production-ready** — FastAPI + Docker + Render deployment
5. **Rich demo** — 3-tab Streamlit UI with Plotly visualizations
6. **Unique angle** — DishaSetu Mode is entirely novel for a hiring hackathon

### Submission Checklist
- [x] Working PoC (FastAPI + Streamlit)
- [x] Semantic matching (Sentence-BERT)
- [x] Hybrid ranking (5 dimensions)
- [x] Decision simulation (DishaSetu Mode)
- [x] Risk detection (4 types)
- [x] Family mode (balance algorithm)
- [x] Bharat knowledge layer (50+ scholarships)
- [x] GitHub Repository (Public)
- [x] README.md (This file)
- [x] WORK_DONE.md (Progress tracker)
- [x] METHODOLOGY.md (Technical deep dive)
- [x] Deployment config (Docker + Render)
- [ ] Demo Video (3-min walkthrough) — Record with OBS/Loom
- [ ] Live deployment — Deploy on Render.com

---

## 👨‍💻 Team

| Name | Role | GitHub |
|:---|:---|:---|
| [Your Name] | AI/ML Engineer & Full Stack | [@github](https://github.com) |
| [Team Member] | Backend Developer | [@github](https://github.com) |
| [Team Member] | Frontend & Design | [@github](https://github.com) |

---

## 📄 License

MIT © 2026 TalentX Team

---

## 🙏 Acknowledgments

- **Redrob AI** for organizing India Runs Hackathon
- **Hack2skill** for the platform
- **Hugging Face** for the Sentence-BERT model (`all-MiniLM-L6-v2`)
- **spaCy** for NLP tooling
- **Streamlit** for the rapid UI framework
- **All Indian students** who deserve better career guidance

---

## 🌟 Star This Repo!

If TalentX helped you or impressed you, please ⭐ the repo!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/talentx?style=social)](https://github.com/yourusername/talentx)

---

**Built with ❤️ for India 🇮🇳 · TalentX – The X Factor in Hiring & Life Decisions**
