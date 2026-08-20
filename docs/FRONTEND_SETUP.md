# JDIS Frontend Setup & Developer Guide

**Target System**: Judicial Delay Intelligence System (JDIS)  
**Stack**: React 18 + TypeScript + Vite + Tailwind CSS + Lucide Icons + Recharts  
**Base Directory**: `frontend/`  

---

## 1. Environment & Prerequisites

- **Node.js**: v18.x or v20.x LTS
- **Package Manager**: `npm` v9.x or later
- **Backend Service**: Namdeo's FastAPI backend running at `http://localhost:8000`

---

## 2. Installation & Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Environment Configuration**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *Default Configuration*:
   ```ini
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   ```

---

## 3. Development Server

To launch the local Vite development server:

```bash
npm run dev
```

The application will be accessible at `http://localhost:3000`. Requests to `/api/v1` and `/health` are automatically proxied to the live backend running at `http://localhost:8000`.

---

## 4. Building for Production

To run TypeScript type-checks and compile the production bundle:

```bash
npm run build
```

To preview the built static bundle locally:

```bash
npm run preview
```

---

## 5. Running Automated Tests

### Unit & Component Tests (Vitest)
```bash
npm run test
```

### End-to-End Smoke Tests (Playwright)
Ensure the backend server (`uvicorn backend.app.main:app`) and frontend dev server (`npm run dev`) are running:

```bash
npm run test:e2e
```

---

## 6. API Client & Endpoint Mapping

All HTTP requests are routed through `src/api/client.ts` which uses Axios with uniform error interceptors:
- `GET /health` -> Backend & ML load state
- `POST /api/v1/predictions/delay` -> Delay classification, calibrated probability, JDIS risk score, top SHAP drivers
- `POST /api/v1/predictions/duration` -> Predicted duration in days with limitation flag
- `GET /api/v1/predictions/{id}/explanation` -> Detailed local SHAP decomposition
- `POST /api/v1/cases` -> Create case record & execute initial prediction
- `GET /api/v1/cases` -> List & filter cases with pagination
- `GET /api/v1/cases/{id}` -> Single case details & prediction history
- `GET /api/v1/analytics/summary` -> High-level aggregate KPIs
- `GET /api/v1/analytics/risk-distribution` -> Risk band distribution
- `GET /api/v1/analytics/courts` -> Court-level throughput analytics
- `GET /api/v1/analytics/case-types` -> Case-type delay metrics
