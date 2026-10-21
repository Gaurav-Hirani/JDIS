# JDIS Demonstration Runbook

A repeatable, end-to-end demonstration scenario for the Judicial Delay Intelligence System (JDIS). Covers backend and frontend startup, navigating the application, and submitting a safe synthetic filing for live model inference.

All commands in this runbook assume you are working from the **repository root** unless a `cd` is shown explicitly.

## 1. Environment Startup

### Start Backend

`requirements.txt` lives at the repository root, not inside `backend/`. Install once, then start the API.

```bash
cd /path/to/JDIS            # repository root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Database — either Docker/Postgres...
docker compose up -d db

# ...or SQLite for a local-only demo (no Docker required):
export DATABASE_URL="sqlite:///./jdis.db"

# Create tables
alembic upgrade head

# Serve the API
uvicorn backend.app.main:app --reload --port 8000
```

Wait for `Application startup complete`. The API is now on `http://localhost:8000`; interactive docs at `http://localhost:8000/docs`.

The backend loads two XGBoost artifacts on startup — both are plain Python files wrapped in scikit-learn, no separate inference service:

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Classifier | `models/final_calibrated_clf.joblib` | P(delay > 24 months), isotonic-calibrated |
| Regressor | `models/best_ablation_reg.joblib` | Expected duration in days |

### Start Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite binds `port: 3000` with `strictPort: true`, so the frontend is always on `http://localhost:3000` — never `5173`. If that port is occupied, Vite exits rather than picking another one, so free the port and retry.

## 2. Navigating the Application

1. Open `http://localhost:3000` in your browser.
2. You land on the **Dashboard** (`/dashboard`), showing system health, live ML metrics and recent cases. The sidebar lists five entries: **Dashboard**, **New Prediction**, **Cases Repository**, **Analytics**, **Methodology & About**.

## 3. Submitting a Demonstration Filing

1. Click **New Prediction** in the sidebar (`/prediction/new`).
2. Use one of the three built-in safe sample presets at the top of the form — click the preset and every one of the 29 filing-stage fields populates itself. This is the intended demo path; the form is pre-filled with preset 1 by default.

   | Preset | `state_code` / `dist_code` / `court_no` | `type_name` | Notable settings |
   | :--- | :--- | :--- | :--- |
   | High Risk Criminal Appeal (Complex Jurisdiction) | `01` / `01` / `01` | `criminal appeal` | `court_prior_delay_rate` 0.72, `court_prior_active_backlog` 3400 |
   | Moderate Risk Commercial Dispute | `02` / `05` / `03` | `commercial suit` | delay rate 0.42, backlog 1100 |
   | Low Risk Fast-Track Bail Petition | `03` / `02` / `02` | `bail application` | delay rate 0.15, backlog 300 |

   Court identifiers are short numeric codes — **not** state/district abbreviations like `MH`/`MH01` and **not** room labels like `C1`.

3. The **Save Case Record to Repository** checkbox is checked by default. Leave it on so the filing appears in Cases Repository afterwards.
4. Click **Run Filing Risk Evaluation**. The button reads *Executing ML Inference...* while the request is in flight.

## 4. Reading the Result

The result page renders three panels in one view — there is no separate *View Explanation* button, the explanation loads inline with the score.

**1. JDIS Risk Score gauge.** Read two numbers, side by side:
- **Raw Model Probability** — the direct XGBoost output.
- **Calibrated Delay Probability** — after isotonic calibration; this is what the risk score is derived from.

The score is `floor(calibrated_probability * 100)`, deterministic, no randomness. Bands are labelled without a "Risk" suffix:

| Band | Score |
| :--- | :--- |
| Low | 0–20 |
| Moderate | 21–50 |
| High | 51–80 |
| Very High | 81–100 |

Different raw probabilities can map to the same calibrated value — the production calibrator is a monotonic stepwise mapping, which is why two filings with different raw outputs may share a score.

**2. Predicted Duration card.** In days from filing. If the duration endpoint is unavailable the card shows `N/A` — it does not substitute a guess. Read the limitation note below the number out loud: the regression arm is an **associational estimate only** and systematically underpredicts extreme outliers (cases over 5 years). R² on the held-out test cohort is negative, and it is reported that way on purpose rather than hidden.

**3. SHAP explanation chart.** Horizontal bars, one per top contributor, rendered directly beneath the score. Red pushes delay risk up, blue pulls it down. Note the feature names — `court_prior_delay_rate`, `type_name`, `court_prior_active_backlog` — these are the historical-throughput and case-category signals that dominate, which is the substantive research finding: filing-stage administrative metadata carries real, measurable signal about eventual delay.

## 5. Analytics and Case Management

1. Click **Analytics** (`/analytics`) — macro statistics over the persisted database: risk distribution across all evaluated cases, top delayed case types, court performance breakdowns.
2. Click **Cases Repository** (`/cases`) — the filing you just submitted is there, created with a UUID-based case ID. Click its ID for the read-only profile; all 29 inputs and the final score are stored in the database.

---
**End of demonstration.**

Two things to flag in any live presentation, because they are the honest parts of this project:

- The classifier (Test 2016: ROC-AUC 0.794, PR-AUC 0.642) is genuinely useful for triage. The duration regressor is not, and says so.
- Model v1.0-config-d was trained on 2010–2014 filings and held out on 2016. It has never seen a 2017-or-later case, and its drift behaviour on newer filings is unknown and unmeasured.
