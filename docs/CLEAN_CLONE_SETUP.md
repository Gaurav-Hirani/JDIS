# Clean Clone Setup Guide

This guide walks a new developer through reproducing the verified local runtime environment from a fresh clone.

## 1. Clone Repository
```bash
git clone https://github.com/Gaurav-Hirani/JDIS.git
cd JDIS
```

## 2. Backend Environment
```bash
# Initialize a Python virtual environment (Python 3.11+ recommended)
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies
```bash
# Installs exact, proven, tested versions of ML tools and the API
pip install -r requirements.txt
```
*Note: We strictly pin NumPy to `<2` and SHAP to `<0.50.0` to resolve known breaking ABI conflicts between PyArrow and NumPy 2.x.*

## 4. Configure Environment Variables
```bash
cp .env.example .env
```
*By default, if the PostgreSQL configuration is left untouched (or if the database connection fails), the `backend/app/core/config.py` uses `sqlite:///./jdis_local.db` as a frictionless development fallback.*

## 5. Initialize Database & Migrations
```bash
# Sets up the schema locally (SQLite default, or PostgreSQL if configured)
PYTHONPATH=. alembic upgrade head
```

## 6. Start Backend API
```bash
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
```
*Wait for the log output: `All ML model artifacts loaded and validated successfully.`*

## 7. Start Frontend Development Server
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

## 8. Verification Checks
- **Health Check**: Visit `http://localhost:8000/api/v1/health`. You should receive an `{"status": "ok", ...}` response confirming the database and 29-feature ML models are loaded.
- **Run Prediction**: Open the frontend (`http://localhost:5173`), navigate to **New Prediction**, enter basic safe values (e.g., `type_name`: "Civil Suit", `state_code`: "MH"), and submit.
- **View Explanation**: On the result page, click **View Explanation** to verify the SHAP API renders successfully without throwing dimensionality errors.
