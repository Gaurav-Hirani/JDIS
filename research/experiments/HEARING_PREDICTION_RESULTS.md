# Hearing Continuation & Next-Listing Prediction Results

## 1. Methodological Reframing: Not "Adjournment Prediction"
This module predicts **Hearing Continuation & Next-Listing Delay**. It does **not** predict "Adjournments."
- **Why**: The dataset does not contain granular records of formal judicial adjournment orders (e.g., Order XVII CPC). It only contains a timeline of listed dates. Calling a normal scheduled gap an "adjournment" is a fatal semantic and legal error.

## 2. Experimental Design
- **Prediction Point**: $T_{\text{last\_list}}$ (The date of the most recent court hearing).
- **Target Variable**: `next_listing_gap_days` (`date_next_list - date_last_list`).
- **Included Cases**: `447,149` (after filtering negatives and missing).
  - Target Distribution:
    - Mean: `18.40 days`
    - Median: `4.00 days`
    - Zeros: `188,179` cases
- **Excluded Cases**:
  - `1,905` cases excluded because no next-listing interval is defined (reached terminal disposition).
  - `212` cases excluded due to chronological impossibility (negative gaps).
- **Leakage Controls**: `date_next_list` and all post-disposal outcomes are strictly excluded from the feature space.
- **Temporal Split**: To maintain chronological validity, splitting was performed on the prediction point (`last_list_year`):
  - **Train**: $\le$ 2017
  - **Validation**: 2018
  - **Test**: 2019

## 3. Model Comparison (Exact Metrics)
Baseline and advanced models were trained to predict the exact gap in days.

### Validation (2018)
| Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| Mean Baseline | 24.77 | 34.89 | -0.0047 |
| Median Baseline | 18.44 | 37.45 | -0.1575 |
| Linear Regression | 20.39 | 36.62 | -0.1072 |
| Decision Tree | 17.93 | 38.76 | -0.2402 |
| XGBoost | 18.42 | 38.47 | -0.2218 |
| Random Forest (Selected) | 17.39 | 38.31 | -0.2112 |

### Final Test (2019 - Held Out)
The best model (Random Forest) was evaluated on the strict out-of-sample 2019 cohort.
| Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| Random Forest | 31.27 | 39.20 | -1.7032 |

## 4. Research Conclusion

**RQ-C1: Can next-listing delay be predicted from information available at the last hearing?**
Under the evaluated feature set and models, exact next-listing delay did not achieve useful out-of-time predictive performance. 

**RQ-C2: Do court/judge historical features improve next-listing prediction?**
No. While historical throughput features (like `court_prior_delay_rate`) were highly predictive of macro-level case duration at the time of filing, they were insufficient to produce useful out-of-time prediction of exact next-listing delay.

**RQ-C3: Which information categories contribute most?**
Because the model fails to find a stable gradient (yielding negative out-of-sample R²), feature attributions are predominantly noise fitting.

**RQ-C4: Does the next-listing model generalize to a temporally later hearing cohort?**
No.

**Negative Empirical Finding Statement:**
The tested case-level and historical metadata features were insufficient to produce useful out-of-time prediction of exact next-listing delay. This does not establish that next-listing delay is inherently unpredictable; it establishes the limitation of the available data/features and tested models.

## 5. Limitations
Unobserved operational variables—such as lawyer scheduling conflicts, judge administrative leave, or daily courtroom diary limits—likely contribute to the difficulty of prediction. The JDIS dataset lacks these micro-level session transcripts.
