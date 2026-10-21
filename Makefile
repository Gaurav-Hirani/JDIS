# JDIS — Judicial Delay Intelligence System
# All commands run from the repository root.

.PHONY: help install install-frontend db-up db-down migrate backend frontend \
       test test-backend test-frontend test-e2e lint build \
       features datasets baselines train train-hearing calibrate shap pipeline \
       docker-build docker-up docker-down

.DEFAULT_GOAL := help

help:
	@echo "JDIS — available targets"
	@echo ""
	@echo "  install           Install Python dependencies"
	@echo "  install-frontend  Install frontend dependencies"
	@echo "  db-up             Start PostgreSQL in Docker"
	@echo "  db-down           Stop PostgreSQL"
	@echo "  migrate           Run alembic upgrade head"
	@echo "  backend           Run FastAPI on :8000 (reload)"
	@echo "  frontend          Run Vite dev server on :3000"
	@echo ""
	@echo "  test              Run all Python tests"
	@echo "  test-backend      Run pytest on tests/"
	@echo "  test-frontend     Run vitest unit tests"
	@echo "  test-e2e          Run Playwright e2e tests"
	@echo "  lint              Run frontend linter"
	@echo "  build             Build frontend production bundle"
	@echo ""
	@echo "  features          Build the 29 Config D features"
	@echo "  datasets          Build final training/val/test datasets"
	@echo "  baselines         Rebuild final baselines"
	@echo "  train             Train the delay classifier + duration regressor"
	@echo "  train-hearing     Train the hearing-gap model"
	@echo "  calibrate         Run isotonic calibration"
	@echo "  shap              Run SHAP attribution extraction"
	@echo "  pipeline          Run all ML pipeline stages in order"
	@echo ""
	@echo "  docker-build      Build the backend image"
	@echo "  docker-up         Run backend + db via docker compose"
	@echo "  docker-down       Tear down the compose stack"

install:
	pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

db-up:
	docker compose up -d db

db-down:
	docker compose down db

migrate:
	alembic upgrade head

backend:
	uvicorn backend.app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

test:
	python -m pytest -q

test-backend:
	python -m pytest tests/ -q

test-frontend:
	cd frontend && npx vitest run

test-e2e:
	cd frontend && npx playwright test

lint:
	cd frontend && npm run lint

build:
	cd frontend && npm run build

# --- ML pipeline ---
# All module invocations must use `python -m` from the repo root.
# Running as `python src/features/build_features.py` sets the script's own
# directory as sys.path[0] and raises ModuleNotFoundError: No module named 'src'.

features:
	python -m src.features.build_features

datasets:
	python -m src.data.create_final_datasets

baselines:
	python -m src.ml.rebuild_final_baselines

train:
	python -m src.ml.train_advanced_models

train-hearing:
	python -m src.ml.train_hearing_advanced

calibrate:
	python -m src.xai.run_calibration

shap:
	python -m src.xai.run_shap

pipeline: features datasets baselines train train-hearing calibrate shap

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down
