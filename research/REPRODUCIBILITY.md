# JDIS Experiment Reproducibility

## 1. Raw Data Source
- **Provider**: Development Data Lab (DDL) e-Courts aggregate
- **Local Raw Archive Names**: `data/extracted/cases_sample/sample_cases_2010.csv`, ..., `sample_cases_2018.csv`
- **Supporting keys**: `data/extracted/keys/`, `data/extracted/judges_clean/judges_clean.csv`, `data/extracted/acts_sections_sample.csv`

## 2. Environment
- **Python Version**: >= 3.9
- **Install**: `pip install -r requirements.txt` (all versions are pinned there)
- **Important Package Versions**:
  - `xgboost == 2.1.4`
  - `scikit-learn >= 1.2.0, <= 1.9.0`
  - `shap >= 0.41.0, < 0.50.0`
  - `lightgbm >= 4.0.0, < 5` (comparison arm in `src/ml/train_advanced_models.py`)
  - `pandas >= 1.5.0`, `numpy >= 1.23.0, < 2`

## 3. Data Processing Commands
- Preprocessing and feature engineering are executed sequentially. All repository
  scripts are invoked as modules from the repository root so that absolute
  `src.*` imports resolve:
  ```bash
  # Stage 1: clean, join, engineer features -> parquet datasets A/B/C
  python -m src.features.build_features

  # Stage 2: derive the censoring-aware training targets (label leakage control)
  python -m src.data.create_final_datasets
  ```
- `build_features.py` writes `data/processed/cases_clean.parquet`,
  `data/features/filing_features.parquet`, `ongoing_features.parquet` and
  `hearing_features.parquet`.
- `create_final_datasets.py` writes `data/features/filing_regression_final.parquet`
  and `data/features/filing_classification_24m_final.parquet`, applying the
  right-censoring rule (unresolved cases are labelled delayed only when
  `follow_up_days > 730.5`, otherwise UNKNOWN and excluded).

## 4. Model Training Commands
- **Baseline comparison arms** (Random Forest, XGBoost, LightGBM, decision trees,
  dummy models, logistic/linear regression):
  ```bash
  python -m src.ml.rebuild_final_baselines
  ```
- **Final advanced model selection** (feature ablation + advanced variants):
  ```bash
  python -m src.ml.train_advanced_models
  ```
- **Hearing-stage model** (Dataset C — research-only negative result):
  ```bash
  python -m src.ml.train_hearing_advanced
  ```
- **Calibration and SHAP explainability**:
  ```bash
  python -m src.xai.run_calibration
  python -m src.xai.run_shap
  ```
- Production artifacts referenced by the backend:
  `models/final_calibrated_clf.joblib` and `models/best_ablation_reg.joblib`.

## 5. Random Seeds
To ensure determinism across Random Forests, XGBoost, and Decision Trees, `random_state=42` is universally applied in all cross-validation blocks and estimators.

## 6. Experiments and the Temporal Split
Random train-test splits are strictly prohibited. The primary filing-time
timeline is 2010–2016:

| Split | Filing years | Purpose |
| :--- | :--- | :--- |
| Train | 2010–2014 | Fitting and ablation selection |
| Validation | 2015 | Hyperparameter tuning and thresholding |
| Test | 2016 | Strictly held out; final evaluation only |

## 7. Experiment Locations
Models and outputs are tracked locally without pushing large binary artifacts to version control:
- Models: `models/*.joblib`
- Output CSVs: `research/results/*.csv`
- Figures: `research/figures/`

*Note: Raw `.csv` and processed `.parquet` datasets are strictly excluded from source control.*
