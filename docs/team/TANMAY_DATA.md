# Tanmay — Data Engineer & Data Architect Execution Guide

**Role**: Data Engineer & Data Architect  
**Project**: Judicial Delay Intelligence System (JDIS)  
**Deliverable Documentation Hub**: `docs/data/`

---

## 1. Role Responsibilities & Workstream Boundaries

Tanmay is solely responsible for the end-to-end data foundation of JDIS. This encompasses:
- Raw archive ingestion & immutable data governance (`data/raw/` -> `data/extracted/`)
- Relational schema normalization, key resolution, and date sanitization
- Feature engineering pipeline (`src/features/`) and historical time-safe windowing
- Data leakage prevention and temporal split integrity (Train: 2010–2016, Val: 2017, Test: 2018)
- Downstream data contracts and ML handoff to Gaurav (`docs/data/ML_HANDOFF.md`)

*Boundaries*: Tanmay does not train final ML models, develop the FastAPI backend (Namdeo), or build the React dashboard (Shukla).

---

## 2. Completed Deliverables & Data Documentation Index

| Deliverable | File Path | Description |
| :--- | :--- | :--- |
| **Dataset & Schema Audit** | [`docs/data/DATASET_SCHEMA_AUDIT.md`](file:///e:/JDIS/docs/data/DATASET_SCHEMA_AUDIT.md) | Comprehensive audit of 80.9M cases, schemas, ER diagrams, coverage, and anomalies |
| **Adjournment Feasibility** | [`docs/data/ADJOURNMENT_FEASIBILITY.md`](file:///e:/JDIS/docs/data/ADJOURNMENT_FEASIBILITY.md) | Assessment of hearing milestones and formulation of Hearing Delay Risk proxy |
| **NLP Feasibility** | [`docs/data/NLP_FEASIBILITY.md`](file:///e:/JDIS/docs/data/NLP_FEASIBILITY.md) | Investigation of text fields; TF-IDF baseline vs BERT feasibility analysis |
| **Graph Feature Feasibility** | [`docs/data/GRAPH_FEATURE_FEASIBILITY.md`](file:///e:/JDIS/docs/data/GRAPH_FEATURE_FEASIBILITY.md) | Assessment of judge/court bipartite networks and litigant anonymization boundaries |
| **Feature Leakage Audit** | [`docs/data/FEATURE_LEAKAGE_AUDIT.md`](file:///e:/JDIS/docs/data/FEATURE_LEAKAGE_AUDIT.md) | 3-tier classification (Filing Safe vs In-Progress vs Prohibited Leakage) |
| **Master Data Dictionary** | [`docs/data/DATA_DICTIONARY.md`](file:///e:/JDIS/docs/data/DATA_DICTIONARY.md) | Complete specification of all raw columns, targets, and engineered features |
| **Data Architecture & Pipeline** | [`docs/data/DATA_PIPELINE.md`](file:///e:/JDIS/docs/data/DATA_PIPELINE.md) | Architecture diagram and scaling strategy (Stage A/B/C) |
| **Data Quality Report** | [`docs/data/DATA_QUALITY_REPORT.md`](file:///e:/JDIS/docs/data/DATA_QUALITY_REPORT.md) | Empirical profiling report across 450k sampled cases and 76M act citations |
| **ML Handoff Contract** | [`docs/data/ML_HANDOFF.md`](file:///e:/JDIS/docs/data/ML_HANDOFF.md) | Data loading instructions, column specifications, and contracts for Gaurav |

---

## 3. Data Engineering Scripts & Utilities

- `scripts/extract_samples.py`: Streaming extractor for multi-year case samples and key tables.
- `scripts/audit_metadata.py`: Profiler for states, districts, court complexes, and judges.
- `scripts/deep_data_audit.py`: Deep schema, missingness, duration, and delay rate auditor.
- `scripts/audit_case_types_and_purposes.py`: Classifier for Civil vs Criminal case types and hearing purpose text.
- `scripts/generate_metrics.py`: Metrics JSON generator for automated quality reporting.

---

## 4. Current Status: Awaiting Approval of Feasibility Audit

In accordance with **Rule 1 and Stop Condition 23**, full pipeline execution and feature matrix exports are paused pending human review and team sign-off on the feasibility findings.
