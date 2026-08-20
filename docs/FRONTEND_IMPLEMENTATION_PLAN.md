# JDIS Frontend Implementation Plan

**Author**: Shukla (Frontend Developer / UX / API Integration)  
**Branch**: `feature/frontend`  
**Target System**: Judicial Delay Intelligence System (JDIS)  
**Date**: 2026-08-20  

---

## 1. Executive Summary & Product Positioning

The **Judicial Delay Intelligence System (JDIS)** frontend provides an interactive, highly polished, and responsive user interface for court administrators, legal researchers, and registry officials. 

### Critical Product Positioning & Governance Guidelines
- **Decision-Support Focus**: JDIS is strictly an administrative decision-support system. It is **NOT** a legal decision-maker, judge replacement, or guarantee of case outcome.
- **Associational Terminology**: All UI labels must strictly convey model probability and risk association. Terms like *"Predicted Delay Probability"*, *"JDIS Risk Score"*, and *"Model Explanation"* must be used instead of *"Guaranteed Delay"* or *"Judge-Caused Delay"*.
- **Non-Causal SHAP Disclaimer**: All SHAP explanation components must include an explicit disclaimer: *"These factors describe statistical model contribution and should not be interpreted as causal effects."*
- **Excluded Features**: Dataset C (Hearing Next-Listing Prediction) is a negative research result ($R^2 = -1.70$) and is **strictly excluded** from production UI workflows.

---

## 2. Technology Stack & Project Architecture

### 2.1 Technology Stack
- **Core Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS + Custom CSS Variables for Design Tokens
- **Icons**: Lucide React
- **Charting**: Recharts (for risk distributions, court metrics, and SHAP horizontal bar charts)
- **Form Management & Validation**: React Hook Form + Zod (aligned with `ML_INFERENCE_CONTRACT.md`)
- **HTTP Client**: Axios with custom interceptors for uniform error handling
- **Testing**: Vitest + React Testing Library + Playwright (E2E)

### 2.2 Directory Structure
The frontend application will be housed inside a top-level `frontend/` directory to cleanly isolate JavaScript/TypeScript code from backend Python modules:

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── .env.example
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── index.css
│   ├── api/
│   │   ├── client.ts             # Axios instance & base URL config
│   │   ├── health.ts             # GET /health
│   │   ├── predictions.ts        # POST /predictions/delay, POST /predictions/duration, GET /predictions/{id}/explanation
│   │   ├── cases.ts              # POST /cases, GET /cases, GET /cases/{id}, PATCH /cases/{id}
│   │   └── analytics.ts          # GET /analytics/summary, /risk-distribution, /courts, /case-types
│   ├── types/
│   │   ├── api.ts                # General API error response types
│   │   ├── prediction.ts         # Feature inputs, prediction outputs, SHAP driver schemas
│   │   ├── case.ts               # Case record and list query params
│   │   └── analytics.ts          # Analytics summaries, court & case type statistics
│   ├── components/
│   │   ├── layout/
│   │   │   ├── LayoutShell.tsx   # Sidebar + Topbar + Content container
│   │   │   ├── Header.tsx        # Title bar + Health indicator
│   │   │   └── Sidebar.tsx       # Navigation links & active state
│   │   ├── common/
│   │   │   ├── HealthIndicator.tsx# Live GET /health connection status pill
│   │   │   ├── RiskBadge.tsx     # Color-coded risk band badge (Low/Moderate/High/Very High)
│   │   │   ├── StatCard.tsx      # Dashboard KPI metric widget
│   │   │   ├── LoadingState.tsx  # Skeleton & spinner loaders
│   │   │   ├── ErrorState.tsx    # Uniform error banner with Retry action
│   │   │   └── EmptyState.tsx    # Empty list fallback state
│   │   ├── prediction/
│   │   │   ├── PredictionForm.tsx# Filing feature entry form (29 fields, Zod validated)
│   │   │   ├── RiskScoreGauge.tsx# Integer 0-100 score + Band display
│   │   │   ├── DurationCard.tsx  # Predicted duration days + limitations flag
│   │   │   └── SHAPChart.tsx     # Horizontal bar breakdown of positive/negative drivers
│   │   ├── cases/
│   │   │   ├── CaseTable.tsx     # Paginated case table with sorting & badges
│   │   │   ├── CaseFilters.tsx   # Search & filter toolbar (State, Court, Case Type, Risk Band)
│   │   │   └── CaseDetailModal.tsx# Case history & detailed prediction drawer
│   │   └── analytics/
│   │       ├── RiskDistChart.tsx # Risk band breakdown donut/bar chart
│   │       ├── CourtMetricsTable.tsx # Court-level caseload & risk summary
│   │       └── CaseTypeBarChart.tsx # Delay rate by case category
│   ├── pages/
│   │   ├── DashboardPage.tsx     # Main executive dashboard
│   │   ├── NewPredictionPage.tsx # Single case prediction form & workflow
│   │   ├── PredictionResultPage.tsx # Detailed view of prediction output & SHAP
│   │   ├── CaseManagementPage.tsx# List, filter, and inspect persisted cases
│   │   ├── AnalyticsPage.tsx     # Deep-dive court & case-type analytics
│   │   └── AboutPage.tsx         # Methodology, governance disclaimers, & research context
│   ├── utils/
│   │   ├── formatters.ts         # Percentages, days to years, numbers, dates
│   │   └── risk.ts               # Color mapping, badge styling, band helpers
│   └── tests/
│       ├── unit/                 # Form validation, risk badge, SHAP chart tests
│       └── e2e/                  # Playwright flow tests
```

---

## 3. Page Structure & User Experience Workflow

| Page | Path | Core Components & Features | Real Backend Endpoints Used |
| :--- | :--- | :--- | :--- |
| **Dashboard** | `/` | System KPIs, Risk distribution donut chart, Recent predictions list, High-risk case alert banner, Quick links to filing prediction. | `GET /health`<br>`GET /analytics/summary`<br>`GET /analytics/risk-distribution`<br>`GET /cases?page=1&page_size=5` |
| **New Prediction** | `/predict` | Structured 29-feature filing form (Case Info, Geography, Acts & Sections, Demographics, Judge & Throughput). Input validation, pre-filled safe sample presets, instant API submission. | `POST /predictions/delay`<br>`POST /predictions/duration`<br>`POST /cases` (Save Option) |
| **Prediction Result**| `/prediction/:id` or inline | Large JDIS Risk Score (0-100), Risk Band Badge, Calibrated Probability %, Expected Duration (Days), Model Version tag, Local SHAP explanation waterfall breakdown. | `GET /predictions/{id}/explanation` |
| **Case Management** | `/cases` | Paginated case repository table, live text search, filter controls (State, Court, Case Type, Risk Band), detail view drawer showing full case filing attributes & prediction history. | `GET /cases`<br>`GET /cases/{id}`<br>`PATCH /cases/{id}` |
| **Analytics** | `/analytics` | System-wide risk distribution, Court-level delay risk ranking table, Case-type delay propensity bar chart, average duration analysis. | `GET /analytics/summary`<br>`GET /analytics/risk-distribution`<br>`GET /analytics/courts`<br>`GET /analytics/case-types` |
| **About / Methodology** | `/about` | JDIS decision-support statement, Isotonic risk calibration methodology, 29 Config D feature spec explanation, Model limitations notice, Dataset C negative result documentation. | Static reference & `GET /health` |

---

## 4. Design System & Risk Theme Specifications

### 4.1 Design System Tokens
- **Primary Theme**: Modern Slate / Indigo Dark-Light theme with clean border hierarchy.
- **Typography**: Inter / System Sans-serif stack for crisp data readability.
- **Risk Colors & Visual Encoding**:

| Risk Band | Integer Score Range | Accent Color | Hex Token | Dark Mode BG | Badge Icon |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Low** | 0 – 20 | Emerald Green | `#10B981` | `rgba(16, 185, 129, 0.15)` | `CheckCircle2` |
| **Moderate** | 21 – 50 | Amber Yellow | `#F59E0B` | `rgba(245, 158, 11, 0.15)` | `AlertTriangle` |
| **High** | 51 – 80 | Orange | `#F97316` | `rgba(249, 115, 22, 0.15)` | `AlertCircle` |
| **Very High** | 81 – 100 | Crimson Red | `#EF4444` | `rgba(239, 68, 68, 0.15)` | `ShieldAlert` |

*Accessibility Guarantee*: Every risk indicator couples the accent color with explicit text labels and icon indicators, ensuring accessibility for colorblind users.

---

## 5. API Endpoints & Request / Response Schemas

### 5.1 Endpoint Mapping Summary
1. `GET /health` -> Connection status & model load check
2. `POST /api/v1/predictions/delay` -> Calibrated delay probability, risk score, band, top SHAP drivers
3. `POST /api/v1/predictions/duration` -> Predicted duration in days + limitations flag
4. `GET /api/v1/predictions/{id}/explanation` -> Detailed SHAP local attribution list
5. `POST /api/v1/cases` -> Create case in DB & trigger prediction
6. `GET /api/v1/cases` -> Paginated case listing with filter parameters
7. `GET /api/v1/cases/{id}` -> Fetch single case record details
8. `GET /api/v1/analytics/summary` -> Aggregate system KPIs
9. `GET /api/v1/analytics/risk-distribution` -> Breakdown across 4 risk bands
10. `GET /api/v1/analytics/courts` -> Court-level throughput & risk statistics
11. `GET /api/v1/analytics/case-types` -> Case-type delay metrics

### 5.2 Form Data Payload Schema (29 Config D Features)
The form payload directly strictly adheres to `ML_INFERENCE_CONTRACT.md`:
```typescript
export interface CaseFilingFeatures {
  // Required Identifiers
  state_code: string;           // Required
  dist_code: string;            // Required
  court_no: string;             // Required
  type_name: string;            // Required

  // Temporal Metadata
  filing_month: number;         // 1..12 (default 1)
  filing_day_of_week: number;   // 0..6 (default 1)
  filing_quarter: number;       // 1..4 (default 1)

  // Case Classification
  case_type_str: string;        // e.g. "criminal"
  case_category: string;       // e.g. "criminal"
  is_criminal_code: number;     // 0 or 1

  // Statutory Details
  statutory_act_count: number;  // >= 0
  ipc_section_count: number;    // >= 0
  bailable_ipc_flag: string;    // "bailable", "non-bailable", "unknown"
  primary_act_id: string;       // e.g. "act_ipc"

  // Demographics & Counsel
  female_defendant_clean: string;  // "0" or "1"
  female_petitioner_clean: string; // "0" or "1"
  female_adv_def_clean: string;    // "0" or "1"
  female_adv_pet_clean: string;    // "0" or "1"

  // Geographical & Court Labels
  state_str: string;            // e.g. "Maharashtra"
  district_str: string;         // e.g. "Mumbai"
  court_str: string;            // e.g. "Chief Metropolitan Magistrate"

  // Judicial Attributes
  ddl_filing_judge_id: string;  // e.g. "judge_101"
  judge_position_clean: string; // e.g. "magistrate"
  judge_gender: string;         // "male", "female", "unknown"
  judge_tenure_days: number;    // >= 0

  // Historical Court Throughput
  court_prior_delay_rate: number;    // 0.0 .. 1.0
  court_prior_avg_duration: number;  // >= 0
  court_prior_active_backlog: number;// >= 0
  casetype_prior_delay_rate: number; // 0.0 .. 1.0
}
```

---

## 6. Form Validation & User Inputs

### 6.1 Validation Logic with Zod
- **Required String Fields**: `state_code`, `dist_code`, `court_no`, `type_name` cannot be blank.
- **Range Constraints**:
  - `filing_month`: Integer between 1 and 12.
  - `filing_day_of_week`: Integer between 0 and 6.
  - `filing_quarter`: Integer between 1 and 4.
  - `is_criminal_code`: Integer 0 or 1.
  - `court_prior_delay_rate`, `casetype_prior_delay_rate`: Float between 0.0 and 1.0.
  - Numeric counts/tenures: Non-negative numbers.
- **Dropdown Control Options**:
  - `bailable_ipc_flag`: `bailable`, `non-bailable`, `unknown`
  - `judge_gender`: `male`, `female`, `unknown`
  - `female_*_clean` flags: `0` (No), `1` (Yes)
  - `is_criminal_code`: `0` (Civil/Other), `1` (Criminal)

---

## 7. State Management & API Integration Strategy

### 7.1 Server State & API Layer
- **Axios Client**: Centralized instance with 10s timeout, JSON headers, and uniform error transformations.
- **Environment Configuration**: API base URL configured via `import.meta.env.VITE_API_BASE_URL`, defaulting to `http://localhost:8000/api/v1`.
- **Error Handling**: API errors (`422 Validation Error`, `404 Not Found`, `500 Server Error`, `Connection Refused`) are parsed and rendered via `<ErrorState />` with retry options.

---

## 8. Charting & Visualization Strategy

1. **SHAP Explanation Chart**:
   - Custom horizontal bar visualization (`SHAPChart.tsx`) powered by Recharts.
   - Positive attributions (driving delay risk *higher*) rendered in Warm Red/Orange.
   - Negative attributions (mitigating delay risk *lower*) rendered in Cool Blue/Teal.
   - Tooltips show exact SHAP value, parent feature category, and human-readable feature descriptions provided by the backend.
2. **Analytics Risk Distribution**:
   - Donut chart displaying proportions of Low, Moderate, High, and Very High risk cases.
3. **Court & Case Type Analytics**:
   - Responsive bar and scatter plots showing high-risk ratio vs average active backlog across courts.

---

## 9. Testing Strategy

### 9.1 Unit & Component Testing (Vitest + React Testing Library)
- **Form Validation Tests**: Verify required field enforcement, out-of-range value blocking, and schema error messages.
- **Risk Score & Band Rendering**: Test that scores 0..20 render Low badge, 21..50 Moderate, 51..80 High, 81..100 Very High with exact colors and accessible text.
- **SHAP Breakdown Tests**: Verify horizontal bars map positive vs negative contributions and show human-readable descriptions.
- **API Client Tests**: Mock Axios endpoints and verify standard error payload handling (e.g. `422 Unprocessable Entity`).

### 9.2 End-to-End Testing (Playwright)
- **Flow 1**: Open Dashboard -> Verify connection indicator green -> Verify system summary metrics.
- **Flow 2**: Navigate to New Prediction -> Fill 29 filing features -> Submit -> Verify Risk Score card (e.g., 81 / Very High), calibrated probability, predicted duration, and SHAP chart.
- **Flow 3**: Navigate to Case Management -> Search by court/case type -> Filter by "Very High" risk band -> Open Case Detail drawer.
- **Flow 4**: Navigate to Analytics -> Verify risk distribution and court rankings render cleanly without fallback errors.

---

## 10. Implementation Phase Roadmap

- **Phase 1**: Architecture Audit & Implementation Plan (Current - COMPLETE)
- **Phase 2**: Scaffold React + Vite + TypeScript application in `frontend/`, configure Tailwind CSS design system & icons.
- **Phase 3**: Implement API client layer (`src/api/`) and TypeScript interfaces (`src/types/`).
- **Phase 4**: Build Layout Shell, Header with live `GET /health` connection status, and Sidebar navigation.
- **Phase 5**: Implement Executive Dashboard page with system KPI cards and risk distribution chart.
- **Phase 6**: Implement 29-feature filing Prediction Form page with Zod validation and safe pre-set samples.
- **Phase 7**: Implement Prediction Result view with integer Risk Score gauge, Risk Band badge, duration card, and SHAP explanation waterfall chart.
- **Phase 8**: Implement Case Management page with search, risk band filters, paginated table, and detail drawer.
- **Phase 9**: Implement Analytics Dashboard page with real backend court & case-type breakdown.
- **Phase 10**: Implement About / Methodology page with governance guidelines and limitations disclaimers.
- **Phase 11**: Add Vitest unit tests and Playwright E2E smoke tests.
- **Phase 12**: Real Backend Runtime Verification & End-to-End Polish.

---
