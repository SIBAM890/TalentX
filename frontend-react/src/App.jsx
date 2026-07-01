import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

const sampleResumes = [
  {
    name: "Rahul Sharma",
    content:
      "Senior Data Scientist with 5 years experience in Python, machine learning, NLP, TensorFlow, SQL, AWS and production model deployment. BTech Computer Science.",
  },
  {
    name: "Priya Mehta",
    content:
      "Data Analyst with 3 years experience in Python, SQL, Tableau, statistics, pandas, scikit-learn and business dashboards. MSc Statistics.",
  },
  {
    name: "Oliver James",
    content:
      "Machine Learning Engineer with 4 years in Python, PyTorch, NLP, recommendation systems, MLOps, Docker and cloud deployment.",
  },
];

const sampleJd =
  "Data Scientist with 3+ years of Python, machine learning, NLP, SQL, model deployment, cloud experience and strong statistics foundation.";

async function postJson(path, payload) {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json();
}

function StatusBar() {
  return (
    <div className="status">
      <span>9:41</span>
      <span className="signal">● ● ●</span>
    </div>
  );
}

function PeopleArt() {
  return (
    <div className="people-art" aria-hidden="true">
      <div className="person left">
        <div className="face" />
        <div className="book" />
      </div>
      <div className="person main">
        <div className="face" />
        <div className="laptop" />
      </div>
      <div className="person right">
        <div className="face" />
        <div className="book" />
      </div>
    </div>
  );
}

function HomeScreen({ setScreen }) {
  return (
    <>
      <StatusBar />
      <header className="topbar">
        <div>
          <h1>TalentX</h1>
          <p>The X Factor in Hiring & Life Decisions</p>
        </div>
        <button className="icon-btn" aria-label="Notifications">
          ◌
        </button>
      </header>

      <PeopleArt />

      <section className="hero-copy">
        <h2>AI-Powered Guidance for Smarter Decisions</h2>
        <p>Career decisions, risk analysis, scholarships and intelligent hiring, all in one place.</p>
      </section>

      <section className="mode-grid">
        <button className="mode-card purple-soft" onClick={() => setScreen("candidate")}>
          <span className="card-icon">◈</span>
          <strong>Candidate Mode</strong>
          <small>Career guidance & decision making</small>
          <b>›</b>
        </button>
        <button className="mode-card orange-soft" onClick={() => setScreen("recruiter")}>
          <span className="card-icon orange">▣</span>
          <strong>Recruiter Mode</strong>
          <small>Candidate ranking & insights</small>
          <b>›</b>
        </button>
      </section>

      <h3 className="section-title">Platform Highlights</h3>
      <section className="stat-grid">
        <article className="stat purple-soft">
          <i>◆</i>
          <strong>15+</strong>
          <span>Career Paths</span>
        </article>
        <article className="stat green-soft">
          <i>▰</i>
          <strong>200+</strong>
          <span>Skills</span>
        </article>
        <article className="stat pink-soft">
          <i>●</i>
          <strong>50+</strong>
          <span>Scholarships</span>
        </article>
        <article className="stat blue-soft">
          <i>●●</i>
          <strong>1000+</strong>
          <span>Resumes</span>
        </article>
      </section>
    </>
  );
}

function CandidateScreen() {
  const [query, setQuery] = useState(
    "I am a BTech CSE student confused between GATE, placements, and higher studies abroad"
  );
  const [background, setBackground] = useState("3rd year BTech CSE, CGPA 8.0, Python and ML basics");
  const [location, setLocation] = useState("Odisha");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit() {
    setLoading(true);
    setError("");
    try {
      const data = await postJson("/api/candidate/decide", {
        query,
        user_background: background,
        location,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <StatusBar />
      <header className="profile-row">
        <div className="avatar">A</div>
        <div>
          <h2>Hi, Ananya!</h2>
          <p>What do you want to explore today?</p>
        </div>
        <button className="icon-btn" aria-label="Notifications">
          ◌
        </button>
      </header>

      <section className="journey-card">
        <div>
          <h3>Your Learning Journey</h3>
          <p>Level 3 · Keep learning!</p>
          <div className="progress-track">
            <span style={{ width: "65%" }} />
          </div>
        </div>
        <div className="target">◎</div>
      </section>

      <h3 className="section-title">My Learning Plan</h3>
      <section className="mini-grid">
        <article className="stat green-soft">
          <i>▰</i>
          <strong>15</strong>
          <span>Career Paths</span>
        </article>
        <article className="stat orange-soft">
          <i>□</i>
          <strong>4</strong>
          <span>Risk Types</span>
        </article>
        <article className="stat blue-soft">
          <i>▣</i>
          <strong>50+</strong>
          <span>Schemes</span>
        </article>
      </section>

      <h3 className="section-title">Quick Activities</h3>
      <section className="activity-grid">
        <article className="activity purple">
          <strong>Compare Paths</strong>
          <span>Cost, growth, time and risk together</span>
        </article>
        <article className="activity orange">
          <strong>Smart Focus</strong>
          <span>Find safer choices and action steps</span>
        </article>
      </section>

      <div className="form-card">
        <label>
          Career dilemma
          <textarea value={query} onChange={(event) => setQuery(event.target.value)} />
        </label>
        <label>
          Background
          <textarea value={background} onChange={(event) => setBackground(event.target.value)} />
        </label>
        <label>
          State
          <input value={location} onChange={(event) => setLocation(event.target.value)} />
        </label>
        <button className="primary-btn" onClick={submit} disabled={loading}>
          {loading ? "Simulating..." : "Simulate My Options"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <section className="results">
          <article className="result-card purple-soft">
            <span>AI RECOMMENDATION</span>
            <h3>{result.recommendation}</h3>
          </article>
          {result.bharat_context && <p className="note">{result.bharat_context}</p>}
          {result.options.map((option, index) => (
            <article className="option-card" key={option.name}>
              <div className="rank-dot">{index + 1}</div>
              <div>
                <h3>{option.name}</h3>
                <p>{option.description}</p>
                <div className="score-row">
                  <span>Cost {Math.round(option.cost_score)}</span>
                  <span>Growth {Math.round(option.growth_score)}</span>
                  <span>{option.risk_level} risk</span>
                </div>
                <strong>{option.expected_salary}</strong>
              </div>
            </article>
          ))}
        </section>
      )}
    </>
  );
}

function RecruiterScreen() {
  const [jd, setJd] = useState(sampleJd);
  const [resumesText, setResumesText] = useState(
    sampleResumes.map((resume) => `${resume.name}\n${resume.content}`).join("\n\n---\n\n")
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const resumes = useMemo(
    () =>
      resumesText
        .split(/\n---\n/g)
        .map((block, index) => {
          const lines = block.trim().split("\n");
          return {
            name: lines[0]?.trim() || `Candidate ${index + 1}`,
            content: lines.slice(1).join("\n").trim() || block.trim(),
          };
        })
        .filter((resume) => resume.content.length > 20),
    [resumesText]
  );

  async function rankCandidates() {
    setLoading(true);
    setError("");
    try {
      const data = await postJson("/api/recruiter/rank", {
        jd_text: jd,
        resumes,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const top = result?.ranked_candidates?.[0];

  return (
    <>
      <StatusBar />
      <header className="leader-header">
        <button className="icon-btn">‹</button>
        <button className="icon-btn">◴</button>
      </header>
      <h1 className="page-title">Learning Leaderboard 🏆</h1>
      <p className="page-subtitle">See who's matching the role today and celebrate the strongest candidates.</p>

      <section className="kpi-grid">
        <article>
          <strong>35%</strong>
          <span>Skill Match</span>
        </article>
        <article>
          <strong>25%</strong>
          <span>Semantic Fit</span>
        </article>
      </section>

      <div className="form-card">
        <label>
          Job description
          <textarea value={jd} onChange={(event) => setJd(event.target.value)} />
        </label>
        <label>
          Resumes
          <textarea value={resumesText} onChange={(event) => setResumesText(event.target.value)} />
        </label>
        <button className="primary-btn orange-btn" onClick={rankCandidates} disabled={loading}>
          {loading ? "Ranking..." : "Rank Candidates"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {top && (
        <section className="leader-card">
          <h2>{Math.round(top.total_score).toLocaleString()}</h2>
          <p>Total Score</p>
          <span className="pill">100% Completed</span>
          <div className="winner">{top.name}</div>
          <div className="podium">
            <div className="step two">2</div>
            <div className="step one">1</div>
            <div className="step three">3</div>
          </div>
        </section>
      )}

      {result?.ranked_candidates?.map((candidate) => (
        <article className="candidate-row" key={candidate.name}>
          <b>#{candidate.rank}</b>
          <div>
            <strong>{candidate.name}</strong>
            <span>{candidate.education_level} · {candidate.years_experience} yrs</span>
          </div>
          <em>{candidate.total_score.toFixed(1)}</em>
        </article>
      ))}
    </>
  );
}

function FamilyScreen() {
  const [studentName, setStudentName] = useState("Rohan");
  const [studentView, setStudentView] = useState(
    "I want to pursue AI research and go abroad for MS at a top US university."
  );
  const [parentView, setParentView] = useState(
    "We want a stable job in India near home. Abroad feels risky because of loans and visa uncertainty."
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit() {
    setLoading(true);
    setError("");
    try {
      const data = await postJson("/api/family/decide", {
        student_name: studentName,
        student_view: studentView,
        parent_view: parentView,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <StatusBar />
      <header className="topbar">
        <div>
          <h1>Family Mode</h1>
          <p>Balance ambition, stability and family realities.</p>
        </div>
        <button className="icon-btn">◌</button>
      </header>

      <section className="journey-card green">
        <div>
          <h3>Find the middle path</h3>
          <p>Student satisfaction + parent confidence + action plan</p>
          <div className="progress-track">
            <span style={{ width: "80%" }} />
          </div>
        </div>
        <div className="target">◇</div>
      </section>

      <div className="form-card">
        <label>
          Student name
          <input value={studentName} onChange={(event) => setStudentName(event.target.value)} />
        </label>
        <label>
          Student view
          <textarea value={studentView} onChange={(event) => setStudentView(event.target.value)} />
        </label>
        <label>
          Parent view
          <textarea value={parentView} onChange={(event) => setParentView(event.target.value)} />
        </label>
        <button className="primary-btn" onClick={submit} disabled={loading}>
          {loading ? "Balancing..." : "Find Balanced Compromise"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <section className="results">
          <article className="result-card green-soft center">
            <span>BALANCED RECOMMENDATION</span>
            <h3>{result.balanced_recommendation}</h3>
            <h2>{Math.round(result.compromise_score)}%</h2>
            <p>Compromise score</p>
          </article>
          <article className="result-card purple-soft">
            <span>KEY INSIGHT</span>
            <p>{result.key_insight}</p>
          </article>
          <div className="satisfaction-grid">
            <article>
              <strong>{result.student_satisfaction}/10</strong>
              <span>{studentName || "Student"}</span>
            </article>
            <article>
              <strong>{result.parent_satisfaction}/10</strong>
              <span>Parents</span>
            </article>
          </div>
          {result.action_steps.map((step, index) => (
            <article className="action-row" key={step}>
              <b>{index + 1}</b>
              <span>{step}</span>
            </article>
          ))}
        </section>
      )}
    </>
  );
}

function App() {
  const [screen, setScreen] = useState("home");

  return (
    <main className="phone-shell">
      {screen === "home" && <HomeScreen setScreen={setScreen} />}
      {screen === "candidate" && <CandidateScreen />}
      {screen === "recruiter" && <RecruiterScreen />}
      {screen === "family" && <FamilyScreen />}
      <nav className="bottom-nav">
        <button className={screen === "home" ? "active" : ""} onClick={() => setScreen("home")}>
          ⌂<small>Home</small>
        </button>
        <button className={screen === "candidate" ? "active" : ""} onClick={() => setScreen("candidate")}>
          □<small>Plan</small>
        </button>
        <button className={screen === "recruiter" ? "active" : ""} onClick={() => setScreen("recruiter")}>
          ♕<small>Rank</small>
        </button>
        <button className={screen === "family" ? "active" : ""} onClick={() => setScreen("family")}>
          ○<small>Family</small>
        </button>
      </nav>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
