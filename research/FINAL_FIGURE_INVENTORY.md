# Final Research Figure & Table Inventory

This document lists the critical visual assets generated during the JDIS predictive modeling project, mapped to their proposed placement in the final IEEE research paper.

## 1. Figures

| Filename | Experiment Context | Demonstration | Inclusion Status | Proposed Section |
| :--- | :--- | :--- | :--- | :--- |
| `calibration_curve_isotonic.png` | Phase 5 Calibration | Shows the probability curve alignment before and after Isotonic scaling on the Validation set. | **Include** | Methodology (Calibration) |
| `risk_band_distribution.png` | Phase 5 Risk Scoring | Visualizes the volume of cases bucketed into Low/Mod/High/Very High vs their actual delay rate in 2016 Test. | **Include** | Results (Risk Triage) |
| `shap_global_bar.png` | Phase 5 XAI | Highlights `type_name` and `court_no` as the dominant predictive inputs. | **Include** | Discussion (Interpretability) |
| `shap_waterfall_case_348579.png` | Phase 5 XAI | A single high-risk case explanation showing the additive math of SHAP values pushing probability up. | **Include** | Discussion (Interpretability) |
| `hearing_gap_residuals.png` | Phase 6 Hearing Prediction | Scatter plot demonstrating severe overprediction on 0-day gaps and underprediction on long-tail delays. | **Include** | Results (Negative Findings) |

## 2. Tables

| Table Title | Experiment Context | Demonstration | Inclusion Status | Proposed Section |
| :--- | :--- | :--- | :--- | :--- |
| **Model Comparison (Classification)** | Phase 3/5 | Shows ROC-AUC/F1 jump from Logistic Regression to XGBoost across Train/Val/Test. | **Include** | Results |
| **Risk Score Map** | Phase 5 | Defines the 0-100 deterministic banding boundaries. | **Include** | Methodology |
| **Negative Results (Regression)** | Phase 4/6 | Shows the negative R² metrics for duration and next-listing prediction. | **Include** | Results |
