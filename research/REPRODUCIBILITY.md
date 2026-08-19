# JDIS Experiment Reproducibility

## 1. Raw Data Source
- **Provider**: Development Data Lab (DDL) e-Courts aggregate
- **Local Raw Archive Names**: `cases_2010.csv`, `cases_2011.csv`, ... `cases_2018.csv`

## 2. Environment
- **Python Version**: >= 3.9
- **Important Package Versions**:
  - `pandas >= 1.5.0`
  - `numpy >= 1.23.0`
  - `scikit-learn >= 1.2.0`
  - `xgboost >= 1.7.0`
  - `shap >= 0.41.0`
  - `pytest >= 7.0.0`

## 3. Data Processing Commands
- Preprocessing and feature engineering are executed sequentially:
  ```bash
  python src/data/prepare_cases.py
  python src/data/build_features.py
  ```

## 4. Model Training Commands
- Experiments are triggered via individual pipeline scripts:
  ```bash
  python src/ml/train_filing_classification.py
  python src/ml/train_filing_regression.py
  python src/ml/train_hearing_advanced.py
  ```

## 5. Random Seeds
To ensure determinism across Random Forests, XGBoost, and Decision Trees, `random_state=42` is universally applied in all cross-validation blocks and estimators.

## 6. Experiment Locations
Models and outputs are tracked locally without pushing large binary artifacts to version control:
- Models: `models/*.joblib`
- Output CSVs: `research/results/*.csv`

*Note: Raw `.csv` and processed `.parquet` datasets are strictly excluded from source control.*
