# Deployment Runbook

This guide covers the deployment strategy for the Judicial Delay Intelligence System (JDIS).

## 1. Prerequisites
- **PostgreSQL**: A running PostgreSQL instance (v13+ recommended).
- **Docker & Docker Compose**: The production stack relies on Docker for containerization.
- **Resources**: At least 2GB of RAM available for the backend to load XGBoost/SHAP models into memory.

## 2. Environment Variables
Before deploying, populate the `.env` file on the host machine. Do not commit this file.
```env
# Required for Production Database
POSTGRES_SERVER="db.example.com"
POSTGRES_PORT=5432
POSTGRES_USER="production_user"
POSTGRES_PASSWORD="secure_password"
POSTGRES_DB="jdis_prod"

# MUST be formatted as a valid JSON Array
BACKEND_CORS_ORIGINS='["https://jdis.yourdomain.com", "http://localhost:3000"]'
```

*Note on Database Fallback: While local development defaults to `sqlite:///./jdis_local.db`, production deployments **must** enforce PostgreSQL connection via the `DATABASE_URL` environment override.*

## 3. Docker Startup
Assuming Docker is available on the deployment machine, run the multi-container stack:
```bash
docker compose up -d --build
```

### Docker Verification Notice
*Docker configuration reviewed but runtime execution could not be verified because Docker daemon was unavailable in the final validation environment.*

## 4. Database Migration
Once the stack is up, apply Alembic migrations against the production PostgreSQL instance. If running within the container:
```bash
docker compose exec backend alembic upgrade head
```

## 5. Health Verification
Verify that the deployed API is healthy and has connected to the production database:
```bash
curl -s https://api.yourdomain.com/api/v1/health
```
Expected Output:
```json
{
  "status": "ok",
  "database": "ok",
  "models": "ok",
  "model_version": "v1.0-config-d"
}
```

## 6. Rollback & Troubleshooting
- **Model Loading Failures**: Check RAM limits. The ML models require approximately 800MB in memory.
- **CORS Errors**: Verify that `BACKEND_CORS_ORIGINS` in your `.env` is a strict, valid JSON array string.
- **Numpy/PyArrow Crashes**: The repository strictly pins `numpy<2` and `shap<0.50.0`. If a pip build overrides this, ABI incompatibilities will crash the API on startup.
- **Rollback**: To rollback an application update, simply execute `git checkout <previous_commit>` and rebuild the Docker images. Database migrations are strictly managed via Alembic.
