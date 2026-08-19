# Phase 6 Final Results: Hearing Continuation & Next-Listing Delay

## 1. Prediction Point
The exact moment the model evaluates data is $T_{\text{last\_list}}$ (the date of the most recent court hearing).

## 2. Target Definition
The regression target is `next_listing_gap_days`, mathematically defined as `date_next_list - date_last_list`.

## 3. Inclusion/Exclusion Criteria
- **Included**: 447,149 cases possessing a valid, non-negative target gap.
- **Excluded (Missing)**: 1,905 records without an observed next listing were excluded from the next-listing regression task because no next-listing interval is defined. (Analysis showed 1,898 of these reached a terminal decision at the last listing).
- **Excluded (Chronological Errors)**: 212 records with negative gaps (`date_next_list < date_last_list`).

## 4. Temporal Split
To guarantee chronological out-of-sample evaluation without data leakage, cases were strictly partitioned by `last_list_year`:
- **Train**: $\le$ 2017
- **Validation**: 2018
- **Test**: 2019

## 5. Models Tested
Baseline Regressors: Mean Baseline, Median Baseline, Linear Regression, Decision Tree.
Advanced Regressors: Random Forest, XGBoost.

## 6. Validation Results (2018)
| Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| Mean Baseline | 24.77 | 34.89 | -0.0047 |
| Median Baseline | 18.44 | 37.45 | -0.1575 |
| Linear Regression | 20.39 | 36.62 | -0.1072 |
| Decision Tree | 17.93 | 38.76 | -0.2402 |
| XGBoost | 18.42 | 38.47 | -0.2218 |
| Random Forest (Selected) | 17.39 | 38.31 | -0.2112 |

## 7. Test Results (2019 Out-of-Sample)
The best model selected on validation (Random Forest) was evaluated exactly once on the held-out test block.
- **MAE**: 31.27
- **RMSE**: 39.20
- **R²**: -1.7032

## 8. Limitations
Unobserved operational variables—such as lawyer scheduling conflicts, judge administrative leave, or daily courtroom diary limits—likely contribute to the difficulty of prediction. The JDIS dataset only aggregates macroscopic administrative case data and lacks these microscopic constraints.

## 9. Negative Finding
The tested case-level and historical metadata features were insufficient to produce useful out-of-time prediction of exact next-listing delay. This does not establish that next-listing delay is inherently unpredictable; it establishes the limitation of the available data/features and tested models.

## 10. Final Conclusion
The Hearing Continuation prediction task constitutes a negative empirical result. The Dataset C module will not be deployed as a production endpoint, preserving system integrity and preventing operational reliance on statistically inadequate heuristics.
