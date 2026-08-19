# JDIS Phase 5: XAI & Risk Score Results

This report provides research interpretation for the Phase 5 XAI, Calibration, and Risk Score generation.

### 1. What are the strongest predictive features?
Based on global SHAP explanations, the variables showing the strongest predictive association with case duration and 24-month delay are the **Historical Court Throughput** features (e.g., `court_prior_delay_rate`, `court_prior_avg_duration`) and the specific **Court Establishment** (`court_str`).

### 2. Which features are associated with higher predicted delay?
High values in historical delay rates (`court_prior_delay_rate`, `casetype_prior_delay_rate`) and larger active backlogs (`court_prior_active_backlog`) are heavily associated with higher predicted probability of delay. Certain court jurisdictions (like specific high-volume district courts) also show a strong positive contribution to the risk score.

### 3. Which features are associated with lower predicted delay?
Cases filed in jurisdictions with historically fast resolution times (low `court_prior_avg_duration`) and cases categorized under fast-track or simple case types (identified via `case_type_str` and `type_name`) show a strong predictive association with a timely resolution, pushing SHAP values negative.

### 4. Is the model well calibrated?
The uncalibrated XGBoost classifier showed moderate miscalibration. After comparing Platt (Sigmoid) scaling and Isotonic Regression on the 2015 Validation set, **Isotonic Regression** was selected as the superior method. Because the calibrator was fitted on the 2015 validation set, those calibration metrics are strictly in-sample. The authoritative assessment relies entirely on the 2016 held-out test set.

### 5. Does calibration improve probability quality?
Yes. Using the authoritative 2016 out-of-sample evaluation, the frozen Isotonic calibrator successfully minimized the Expected Calibration Error (ECE) and improved the Brier Score compared to the uncalibrated baseline, ensuring that a predicted probability closely mirrors the empirically observed delay rate.

### 6. What does the 0–100 risk score mean?
The 0–100 JDIS Risk Score is a direct, monotonic integer mapping (`floor(probability * 100)`) of the calibrated delay probability. A score of 75 means the model estimates a 75% probability that the case will take longer than 24 months to resolve. It is divided into interpretable bands (Low: 0-20, Moderate: 21-50, High: 51-80, Very High: 81-100).

### 7. What are the main error patterns?
The classification model struggles primarily with **False Positives** near the decision boundary (cases predicted to delay that resolve on time, often due to sudden court settlements). For regression, the model systematically **underpredicts** extreme outliers (cases lasting > 5 years) because the XGBoost trees compress the extreme tail of the distribution to minimize overall MSE/MAE.

### 8. Where does the model perform poorly?
Performance degrades on "Long (>3 yrs)" cases in exact duration prediction (Regression), where the Mean Absolute Error is substantially higher. The model cannot anticipate external, post-filing factors (like repeated adjournments or appeals) that artificially extend a case.

### 9. Are there meaningful subgroup differences?
Error analysis reveals differing False Discovery Rates across states and court groups. Certain states show a higher False Negative rate, suggesting their unique procedural delays are not fully captured by the historical throughput window.

### 10. What limitations must be reported?
These predictions represent purely associational observed patterns at the time of filing, not causal facts. The model is blind to post-filing events (strikes, specific judge transfers, complex discovery). Outlier duration predictions are systematically conservative. The risk score must be used for triage and resource allocation, never as a definitive judgment on the complexity or merit of an individual case.
