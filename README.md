# 🔮 ChurnGuard AI — Customer Churn Prediction System

An end-to-end machine learning web application that predicts whether a customer
is likely to churn, served through a beautiful Gradio interface backed by a
FastAPI inference microservice — fully containerized and deployed on Render.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-6.x-F97316?logo=gradio&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Ensemble-EB5E31)

---

## 🌐 Live Demo

| Service | URL | Notes |
|---------|-----|-------|
| 🎨 **Web App** | https://churnguard-ui.onrender.com | Prediction form + insights dashboard |
| ⚙️ **API Docs** | https://churnguard-api.onrender.com/docs | Interactive Swagger UI |
| ❤️ **Health** | https://churnguard-api.onrender.com/health | Uptime monitor endpoint |

> Free-tier containers sleep when idle — first request after a pause may take
> ~30s to wake. Keep-alive pings every 10 minutes prevent this.

---

## ✨ Features

| | |
|---|---|
| 🔮 **Instant Prediction** | 16 customer attributes → churn verdict with confidence gauge in under a second |
| 📊 **Model Insights Dashboard** | Live accuracy / precision / recall / F1, confusion matrix, feature importance |
| 📈 **Data Visualisations** | Interactive Plotly charts: churn split, age, tenure & billing distributions |
| 🎨 **Polished UI** | Custom gradient theme, animated result cards, responsive two-column layout |
| 🐳 **One-command Deploy** | `docker compose up` spins up API + UI containers together |

## 🏗️ Architecture

```
┌─────────────────────┐         POST /predict          ┌──────────────────────┐
│   Gradio UI :7860   │ ─────────────────────────────► │   FastAPI API :8000  │
│  (ChurnGuard AI)    │ ◄───────────────────────────── │                      │
│  prediction +       │        JSON {label,            │  Pydantic validation │
│  insights dashboard │         confidence}            │  + feature engine    │
└─────────────────────┘                                └──────────┬───────────┘
                                                                  │
                                                       ┌──────────▼───────────┐
                                                       │  ML Model (.joblib)  │
                                                       │  BaggingClassifier   │
                                                       │  └─ XGBoost ×150     │
                                                       │  sklearn Pipeline    │
                                                       │  (OHE·TargetEnc·     │
                                                       │   Winsorize·Scale)   │
                                                       └──────────────────────┘
```

## 🚀 Quick Start

### Option 1 — Docker (recommended)

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| 🎨 Web UI | http://localhost:7860 |
| ⚙️ API docs (Swagger) | http://localhost:8000/docs |

### Option 2 — Local development

```bash
# Terminal 1 — inference API
pip install -r requirements-api.txt
uvicorn app:app --reload

# Terminal 2 — web UI
pip install -r ui/requirements.txt
python -m ui.app
```

### Option 3 — Deploy to Render (Blueprint, 1 click)

1. Push this repo to GitHub
2. Render dashboard → **New → Blueprint** → select the repo → **Apply**
3. Both services (`api` + `ui`) are created automatically from `render.yaml`
4. Add free keep-alive monitors at [cron-job.org](https://cron-job.org):
   - `https://<api-url>/health` every 10 min
   - `https://<ui-url>` every 10 min

> The Insights tab is powered by a precomputed payload (`ui/insights.json`,
> regenerate with `python scripts/export_insights.py`) so it renders instantly
> even after cold starts on the free tier.

## 🧠 The Model

- **Algorithm**: `BaggingClassifier` wrapping 150 `XGBClassifier` estimators
- **Preprocessing**: median/mean imputation with missing indicators,
  winsorization (5 %/95 %), log-transform on age, one-hot + target encoding,
  standard scaling — all inside a single reproducible `sklearn.Pipeline`
- **Test performance**: ~74 % accuracy with balanced precision/recall
  *(exact live metrics rendered in the Insights tab)*
- **Decision threshold**: tuned at `p(churn) ≥ 0.4658`

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Service status check |
| `GET`  | `/model_load` | Verifies the model artifact loads |
| `POST` | `/predict` | Customer JSON → `{label, confidence}` |
| `GET`  | `/docs` | Interactive Swagger documentation |

Example request:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "age": 34, "gender": "female", "location": "mumbai",
  "tenure_months": 35.7, "monthly_charges": 40.9, "total_charges": 1462.9,
  "contract_type": "monthly", "internet_service": "fiber optic",
  "phone_service": "yes", "online_security": "no", "tech_support": "yes",
  "payment_method": "electronic check", "satisfaction_score": 8,
  "support_tickets": 3, "last_contact_date": "2026-08-25",
  "email": "anita19@yahoo.com"
}'
```

```json
{ "label": "no", "confidence": 0.561 }
```

## 📁 Project Structure

```
.
├── app.py                  # FastAPI service (CORS enabled)
├── src/
│   ├── schema.py           # Pydantic model: validation + feature engineering
│   ├── preprocessing.py    # Winsorization transformer
│   └── model.py            # Training pipeline definition
├── ui/
│   ├── app.py              # Gradio interface (prediction + dashboard tabs)
│   └── insights.json       # Precomputed dashboard payload (instant cold start)
├── scripts/
│   └── export_insights.py  # Regenerates the dashboard payload
├── models/                 # Trained pipeline artifact (.joblib)
├── data/                   # Clean training dataset (~20 k customers)
├── requirements-api.txt    # API service dependencies
├── Dockerfile.api          # FastAPI container
├── Dockerfile.ui           # Gradio container
├── docker-compose.yml      # Local multi-service orchestration
└── render.yaml             # Render Blueprint (one-click deploy)
```

## 🛠️ Tech Stack

**ML**: scikit-learn · XGBoost · imbalanced-learn · joblib
**Backend**: FastAPI · Pydantic v2 · Uvicorn
**Frontend**: Gradio 6 · Plotly · custom CSS
**DevOps**: Docker · Docker Compose

---

<p align="center">Built with ❤️ as an end-to-end MLOps portfolio project</p>
