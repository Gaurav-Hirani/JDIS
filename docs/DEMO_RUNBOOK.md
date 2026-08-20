# JDIS Demonstration Runbook

This guide outlines a repeatable, end-to-end demonstration scenario for the Judicial Delay Intelligence System (JDIS). It covers backend and frontend startup, navigating the application, and submitting a safe, synthetic demonstration case for ML prediction.

## 1. Environment Startup

### Start Backend
Open a terminal and start the FastAPI backend server (which loads the PyTorch/XGBoost models and serves the API):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start PostgreSQL Database (if using Docker)
# docker compose up -d db

# Run migrations (if necessary)
alembic upgrade head

# Start API
uvicorn app.main:app --reload --port 8000
```
*Wait for the `Application startup complete` message. The backend API is now running at `http://localhost:8000`.*

### Start Frontend
Open a second terminal window and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```
*The frontend will compile and start at `http://localhost:3000` or `http://localhost:5173`.*

## 2. Navigating the Application

### Open Application
1. Open your web browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
2. You will be greeted by the **Executive Dashboard**, which displays system health, live ML metrics, and overall analytics.

### Enter Demonstration Case
1. Click on **New Prediction** in the navigation menu.
2. Fill out the 29-feature form using the following safe, synthetic data. This represents a typical civil case scenario:
   - **Case Type (`type_name`)**: `Civil Suit`
   - **State Code (`state_code`)**: `MH`
   - **District Code (`dist_code`)**: `MH01`
   - **Court ID (`court_no`)**: `C1`
   - **Filing Month (`filing_month`)**: `6`
   - **Statutory Acts (`statutory_act_count`)**: `2`
   - **Prior Court Backlog (`court_prior_active_backlog`)**: `5000`
   - *(Leave other demographic and historical inputs at their default median values)*

## 3. Reviewing Predictions

### Submit Prediction & View Risk Score
1. Click **Run Prediction Pipeline**.
2. The UI will call the backend API and return the prediction results.
3. Observe the **Risk Band** (e.g., "High Risk" or "Moderate Risk") and the **Risk Score** (0-100). This indicates the calibrated probability of the case exceeding 24 months of delay.

### View SHAP Explanation
1. On the results screen, click **View Explanation**.
2. A SHAP (SHapley Additive exPlanations) waterfall or bar chart will appear.
3. Note the human-readable features (e.g., `type_name`, `court_no`) and observe their positive (red) or negative (blue) contribution to the overall delay risk.

### View Duration Prediction
1. Scroll down to the **Expected Duration** section.
2. The UI will display a prediction (e.g., "450 Days").
3. **Note the Limitation Warning**: Point out the disclaimer below the metric stating that the regression model systematically underpredicts extreme outliers (cases > 5 years).

## 4. Analytics and Case Management

### Open Dashboard Analytics
1. Click on **Analytics** in the navigation menu.
2. View the macro-level statistics generated from the database: Risk Distribution across all evaluated cases, top delayed case types, and court performance breakdowns.

### Open Case Details
1. Click on **Case Management** or **Case Repository** in the navigation menu.
2. The table will list previously evaluated cases.
3. Click on the ID of the synthetic case you just created to view its permanent read-only profile. All inputs and the final risk score are saved successfully in the backend PostgreSQL/SQLite database.

---
**End of Demonstration.**
