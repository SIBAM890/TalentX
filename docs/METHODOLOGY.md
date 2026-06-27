# 🔬 METHODOLOGY.md – TalentX Technical Deep Dive

> **Project:** TalentX – The X Factor in Hiring & Life Decisions  
> **Track:** India Runs Hackathon – Track 1: Data & AI Challenge

---

## 1. Introduction

TalentX is built on two core thesis statements:

1. **Hiring is broken**: Keyword-based ATS systems are rejecting 70% of qualified candidates. A semantic, multi-dimensional ranking approach recovers hidden talent.

2. **Career decisions need simulation, not advice**: Indian students are told "do engineering" or "study abroad" without data. TalentX replaces opinion with simulation.

---

## 2. Problem Analysis

### 2.1 Recruiter Side
Traditional ATS systems:
- Use Boolean keyword matching (Python AND ML AND SQL)
- Cannot understand synonyms (ML Engineer ≈ Data Scientist)
- Cannot assess contextual fit (relevant projects, domain experience)
- Rank by years of experience only, ignoring growth trajectory

**TalentX's approach**: Replace keyword Boolean with semantic cosine similarity and add 4 additional scoring dimensions.

### 2.2 Candidate Side
Indian students face:
- Information asymmetry (no real outcome data)
- Societal pressure without financial analysis
- Family dynamics that are culturally specific
- India-specific context (state scholarships, PSU eligibility, regional job markets)

**TalentX's approach**: Simulate options computationally, quantify risk, generate year-by-year timelines.

---

## 3. Algorithm Details

### 3.1 Semantic Similarity (Sentence-BERT)

**Model**: `all-MiniLM-L6-v2` from Hugging Face  
**Why**: 384-dim embeddings, 5x faster than BERT-base, strong performance on semantic similarity

```
JD_embedding = SBERT.encode(jd_text)        # 384-dim vector
Resume_embedding = SBERT.encode(resume_text) # 384-dim vector
similarity = cosine_similarity(JD_embedding, Resume_embedding)
```

**Cosine Similarity Formula:**
```
sim(A, B) = (A · B) / (||A|| × ||B||)
```

Range: 0.0 to 1.0. In practice, 0.7+ indicates strong contextual match.

**Fallback**: When SBERT unavailable, uses TF-IDF with 5000 features and n-gram range (1,2).

### 3.2 Hybrid Ranking Formula

```
Total Score = 
    0.35 × Skill_Match +
    0.25 × Semantic_Similarity × 100 +
    0.20 × Experience_Fit +
    0.10 × Education_Fit +
    0.10 × Keyword_Coverage × 100
```

**Skill Match (35%)**:
```
skill_match = (|JD_skills ∩ Resume_skills|) / |JD_skills| × 100
```

**Experience Fit (20%)**:
```
if actual_years >= required_years * 1.5: score = 100
elif actual_years >= required_years:     score = 90 + delta * 2
elif actual_years >= required_years*0.7: score = 70 + (ratio * 20)
elif actual_years > 0:                   score = 40 + (ratio * 30)
else:                                    score = 20 (fresher)
```

**Education Fit (10%)**:
```
PhD → 100 | M.Tech/M.Sc → 85 | B.Tech/B.E → 70 | Diploma → 50
```

**Keyword Coverage (10%)**:
```
coverage = |JD_keywords ∩ Resume_tokens| / |JD_keywords|
```

### 3.3 Risk Scoring Algorithm

Each risk type has:
- A base score (10–20)
- Signal keywords (10–16 per type)
- A bump per matched signal (8–15 points)
- A cap at 100

```
risk_score = min(100, base + bump × matched_signals)
overall_risk = average(financial, skill_gap, market, time)
```

### 3.4 Decision Option Detection

Query → keyword tokenization → option_keyword_map lookup → confidence scoring

```python
confidence = 60 + 15 * (option_key in query) + 2 * positive_signals
```

Options sorted by:
```
desirability = (growth_score + cost_score - risk_score) / 3
```

### 3.5 Family Balance Algorithm

```
student_priority = argmax(keyword_count, STUDENT_SIGNALS)
parent_priority = argmax(keyword_count, PARENT_SIGNALS)

compromise = lookup(COMPROMISES, student_priority, parent_priority)

student_satisfaction = 6.0 + 0.5 × student_signals_in_compromise
parent_satisfaction = 6.0 + 0.5 × parent_signals_in_compromise

compromise_score = (student_satisfaction + parent_satisfaction) / 2 × 10
```

---

## 4. Data Sources

| Data | Source | Size |
|:---|:---|:---:|
| Skill Taxonomy | Curated from LinkedIn Jobs, NASSCOM, Naukri.com | 200+ skills |
| Career Paths | Glassdoor India, Naukri, LinkedIn salary data | 15 paths |
| Scholarships | National Scholarship Portal, State portals | 50+ schemes |
| Career Outlook | NASSCOM, LinkedIn Economic Graph India | 15 domains |
| Sample Resumes | Synthetically generated (representative profiles) | 10 resumes |
| Sample JD | Based on real Data Scientist JDs from Naukri/LinkedIn | 1 JD |

---

## 5. Evaluation Metrics

### Ranking Quality
- **Correctness**: Does strong candidate always rank above weak? (100% in testing)
- **Spread**: Are scores well-distributed (not all bunched near 50)?
- **Explainability**: Can every score be attributed to a specific dimension?

### Semantic Quality
- **Relatedness test**: Data Science JD vs ML resume → should score > 0.70
- **Unrelatedness test**: Data Science JD vs Chef resume → should score < 0.40

### Decision Quality
- **Coverage**: At least 2 meaningful options extracted from any query
- **Ordering**: Higher growth + lower risk options rank first

---

## 6. Ethical Considerations

1. **No bias amplification**: Skill matching is objective (taxonomy-based), not inferred from protected characteristics
2. **Explainability**: Every score is decomposed — no black box
3. **India-first fairness**: Recognizes diverse educational paths (diploma, BCA, state university)
4. **No discrimination**: Education score is one dimension (10%) only; skill and semantic dominate
5. **Data privacy**: No personal data stored; all processing is stateless
6. **Scholarship equity**: Specifically includes SC/ST/OBC/minority/girl-child scholarships

---

## 7. Future Scope

| Enhancement | Technology | Impact |
|:---|:---|:---|
| LLM-enhanced explanations | GPT-4o / Gemini Pro | Richer decision narratives |
| PDF resume parsing | pypdf2, pdfminer | Remove manual text input |
| Hindi language support | IndicBERT, mBERT | Reach tier-2/3 India |
| Resume scoring feedback loop | RLHF | Improve over time |
| LinkedIn integration | LinkedIn API | Real-time candidate data |
| Government scheme API | NIC / MeitY | Auto-updated scholarships |
| Voice query input | Whisper ASR | Accessibility for rural India |
| Multilingual NLP | AI4Bharat IndicNLP | 22 Indian languages |
