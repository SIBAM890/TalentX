# 🚀 DEPLOYMENT.md – TalentX Deployment Guide

---

## Local Development

### 1. Setup

```bash
git clone https://github.com/yourusername/talentx.git
cd talentx
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
```

### 2. Validate Data
```bash
python scripts/seed_data.py
```

### 3. Run API
```bash
uvicorn app.main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

### 4. Run Frontend
```bash
streamlit run frontend/app.py
# UI: http://localhost:8501
```

---

## Docker Deployment

```bash
# Build and run
docker-compose up --build

# API:      http://localhost:8000
# Frontend: http://localhost:8501
```

---

## Render.com Deployment

1. Fork this repository
2. Create a new Web Service on Render.com
3. Connect your GitHub repo
4. Use settings from `render.yaml`:
   - Build: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

---

## Streamlit Community Cloud

1. Go to https://share.streamlit.io
2. Connect GitHub repo
3. Set Main file path: `frontend/app.py`
4. Add packages: `requirements.txt`

---

## Environment Variables

| Variable | Default | Description |
|:---|:---|:---|
| APP_ENV | development | App environment |
| APP_PORT | 8000 | API port |
| SENTENCE_BERT_MODEL | all-MiniLM-L6-v2 | SBERT model name |
| SPACY_MODEL | en_core_web_sm | spaCy model |
| API_BASE_URL | http://localhost:8000 | Frontend → API URL |
