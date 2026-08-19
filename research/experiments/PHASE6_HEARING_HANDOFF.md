# JDIS Phase 6: Hearing Prediction Handoff

## 1. Scope & Terminology
- **Module**: Hearing Continuation & Next-Listing Delay Prediction.
- **Terminology Rule**: The term "Adjournment Prediction" is strictly forbidden due to lack of explicit label validity.

## 2. Experimental Design
- **Dataset**: `data/features/hearing_features.parquet` (Dataset C).
- **Target**: `next_listing_gap_days` (`date_next_list - date_last_list`).
- **Prediction Point**: $T_{\text{last\_list}}$
- **Temporal Split**: Based on `date_last_list_dt.year`
  - Train: $\le$ 2017
  - Val: 2018
  - Test: 2019

## 3. Final Model & Artifacts
- **Algorithm**: Random Forest Regressor
- **Artifact Path**: `models/final_hearing_model.joblib`
- **Features Used**: All non-leaking columns from Dataset C (Tier A + Tier B). Excludes target dates and decisions.

## 4. Empirical Conclusion & Limitations
The tested case-level and historical metadata features were insufficient to produce useful out-of-time prediction of exact next-listing delay (Test R² = -1.70). This does not establish that next-listing delay is inherently unpredictable; it establishes the limitation of the available data/features and tested models.

**Production Decision**:
Dataset C should NOT be exposed as a production prediction module because its final out-of-time performance is inadequate. It is documented formally as an **Evaluated research module / negative experimental result.**

Phase 6 is complete. Await human review before proceeding to any backend or frontend integration.
