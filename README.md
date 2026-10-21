# Judicial Delay Intelligence System (JDIS)

An explainable, censoring-aware machine learning framework that predicts whether a
case filed in an Indian district court will take longer than 24 months to dispose of.

The model works entirely from **filing-time administrative metadata** — the 29 fields
that exist the moment a case is registered. It does not wait for hearings, orders, or
disposition data. That constraint is the point: the system is meant to inform backlog
management *at filing*, when early triage decisions actually still have leverage.

> **This is a decision-support system, not a prediction of outcome.** It estimates the
> probability of procedural delay from historical court throughput patterns. It says
> nothing about the merits, the likely decision, or the rights of any party. See
> [`docs/ETHICS_AND_LIMITATIONS.md`](docs/ETHICS_AND_LIMITATIONS.md).

---

## The research question

Given only what a clerk knows at the filing counter — which court, which judge, what
category of case, how long that court has historically taken — how much real signal is
there about eventual delay?

On a strict temporal holdout (filings from 2016, trained only on 2010–2014), the answer
is "a moderate, usable amount":

| Metric | Value |
| :--- | :--- |
| ROC-AUC | 0.7938 |
| Precision-Recall AUC | 0.6423 |
| Accuracy | 0.7346 |
| F1 | 0.5157 |
| Brier score | 0.1734 |
| Expected Calibration Error | 0.0453 |

The duration regressor and the hearing-gap model are **not** useful, and their negative
R² values are published rather than suppressed. That honesty is the methodological
contribution as much as the classifier is.

## Risk score

The reported score is deterministic and derived from the calibrated probability, not
the raw model output:

```
risk_score = floor(calibrated_probability * 100)
```

| Band | Score range |
| :--- | :--- |
| Low | 0–20 |
| Moderate | 21–50 |
| High | 51–80 |
| Very High | 81–100 |

Two filings with different raw model outputs can legitimately share a score: the
production calibrator is a monotonic stepwise (isotonic) mapping.

## Method in one paragraph

449,266 case records, filtered to a strict temporal split — **train 2010–2014,
validation 2015, test 2016** — with random splits prohibited. Unresolved cases are
right-censored: a case is labelled delayed only if it had been pending for more than
730.5 days at extraction, otherwise it is excluded as unknown. An XGBoost classifier
is isotonic-calibrated against the validation cohort; a separate XGBoost regressor
handles duration. SHAP TreeExplainer produces per-prediction attributions mapped back
to human-readable feature groups.

## Tech stack

**ML / research** — Python 3.11, pandas, scikit-learn, XGBoost 2.1.4, SHAP, LightGBM 4.x

**Backend** — FastAPI, SQLAlchemy 2, Alembic, PostgreSQL (SQLite fallback for local dev)

**Frontend** — React 18.3.1, TypeScript 5.5, Vite 5.4, Tailwind CSS 3.4.9, Recharts 2.12.7, react-hook-form + zod

**Testing** — pytest, Vitest, Playwright (msedge channel)

**Deployment** — Docker, docker-compose

## Repository layout

```
backend/          FastAPI application: routers, services, schemas, models, ML manager
src/              Research pipeline: data cleaning, feature builds, training, XAI
alembic/          Database migration scripts
models/           Frozen production artifacts (.joblib)
configs/          Experiment and ablation configurations
data/             Raw extracts, processed tables, feature datasets
research/         Experiment runners, metric outputs, figures
docs/             Architecture, data dictionary, deployment, ethics
frontend/         React application
tests/            Backend and pipeline test suites
```

## Quick start

All commands assume you are at the **repository root**. `requirements.txt` lives here,
not inside `backend/`.

### Backend

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Database — either Docker/Postgres...
docker compose up -d db

# ...or SQLite, no Docker required:
export DATABASE_URL="sqlite:///./jdis.db"

alembic upgrade head
uvicorn backend.app.main:app --reload --port 8000
```

Wait for `Application startup complete`. The API serves two artifacts loaded once at
startup — `models/final_calibrated_clf.joblib` (classifier) and
`models/best_ablation_reg.joblib` (regressor) — so no separate inference service is
involved.

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite binds port **3000** with `strictPort: true`, so the app is always at
`http://localhost:3000` — never 5173. If that port is occupied, Vite exits rather than
falling back to another port.

## Running the ML pipeline

Every pipeline script is a package module and must be invoked with `python -m` from the
repository root. Running them as files (`python src/features/build_features.py`) fails
with `ModuleNotFoundError: No module named 'src'`, because the script's own directory —
not the repository root — becomes `sys.path[0]`.

```bash
python -m src.features.build_features
python -m src.data.create_final_datasets
python -m src.ml.rebuild_final_baselines
python -m src.ml.train_advanced_models
python -m src.ml.train_hearing_advanced
python -m src.xai.run_calibration
python -m src.xai.run_shap
```

Inputs are the per-year case extracts under `data/extracted/cases_sample/` plus the
key, judge, and act/section lookup tables. Exact commands, versions, and the censoring
rule are in [`research/REPRODUCIBILITY.md`](research/REPRODUCIBILITY.md).

## Testing

```bash
pytest -q                                    # both suites (tests/ + backend/tests/)
python -m pytest tests/ -q
python -m pytest backend/tests/ -q

cd frontend
npx vitest run                               # unit tests
npm run build                                # TypeScript + production bundle
npx playwright test                          # e2e, starts Vite automatically
```

## Documentation

| Document | Contents |
| :--- | :--- |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design |
| [`docs/API_SPECIFICATION.md`](docs/API_SPECIFICATION.md) | Every endpoint, schema, and status code |
| [`docs/ETHICS_AND_LIMITATIONS.md`](docs/ETHICS_AND_LIMITATIONS.md) | Scope, censoring, known failures |
| [`docs/DEMO_RUNBOOK.md`](docs/DEMO_RUNBOOK.md) | End-to-end demonstration script |
| [`docs/DATA_PIPELINE.md`](docs/DATA_PIPELINE.md) | Data flow and quality gates |
| [`docs/data/DATA_DICTIONARY.md`](docs/data/DATA_DICTIONARY.md) | Column-level definitions |
| [`docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md`](docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md) | Inference contract |
| [`docs/data/FINAL_MODEL_FEATURE_SPECIFICATION.md`](docs/data/FINAL_MODEL_FEATURE_SPECIFICATION.md) | The 29 Config D features |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Containerised deployment |
| [`research/REPRODUCIBILITY.md`](research/REPRODUCIBILITY.md) | Exact reproduction steps |

> Note: `docs/data/ML_HANDOFF.md` is **superseded** — it describes an earlier
> three-cohort split that the shipped model does not use. Read
> `FINAL_ML_HANDOFF_TO_BACKEND.md` instead.
