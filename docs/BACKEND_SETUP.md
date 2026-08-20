# JDIS Backend Development Setup Guide

## 1. Environment Setup

### Prerequisites
- Python >= 3.10
- PostgreSQL >= 14 (or SQLite for quick local test fallback)
- Docker & Docker Compose (optional for containerized deployment)

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate environment (Linux/macOS)
source .venv/bin/activate

# Install backend dependencies with pinned XGBoost 2.1.4
pip install -r requirements.txt
```

---

## 2. Configuration & Environment Variables

Copy the sample environment file to `.env`:
```bash
cp .env.example .env
```

Key environment variables in `.env`:
- `DATABASE_URL`: PostgreSQL connection string (`postgresql://user:password@localhost:5432/jdis_db`)
- `MODEL_CLASSIFIER_PATH`: `models/final_calibrated_clf.joblib`
- `MODEL_REGRESSOR_PATH`: `models/best_ablation_reg.joblib`
- `MODEL_VERSION`: `v1.0-config-d`

---

## 3. Database & Migrations

```bash
# Run database migrations with Alembic
PYTHONPATH=. alembic upgrade head

# Generate a new migration if models change
PYTHONPATH=. alembic revision --autogenerate -m "description_of_change"
```

---

## 4. Running the API Server

```bash
# Run Uvicorn development server
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
```

Access:
- API Base: `http://localhost:8000/api/v1`
- Health Check: `http://localhost:8000/health`
- Swagger UI Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

---

## 5. Running Automated Backend Tests

```bash
# Execute the full backend test suite (unit, API, DB, and ML integration)
PYTHONPATH=. pytest backend/tests/ -v
```

---

## 6. Docker Container Deployment

```bash
# Build and start FastAPI and PostgreSQL services
docker-compose up -d --build

# View container logs
docker-compose logs -f backend

# Stop services
docker-compose down
```
