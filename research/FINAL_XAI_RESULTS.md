# Final XAI Results

## 1. Top Predictive Parent Concepts
SHAP global attributions show that historical throughput and specific procedural jurisdictions have the strongest predictive associations.
1. `type_name` (Granular case type name identifier)
2. `case_type_str` (Standardized case type string)
3. `ddl_filing_judge_id` (Filing judge identifier)
4. `court_no` (Numeric court identifier)
5. `court_str` (Court establishment name string)

## 2. Global Explanation
The model primarily differentiates delay probability based on structural categorical identities (case type, court, judge) rather than continuous numeric variables. High historical delay rates push probability scores strictly higher.

## 3. Local Explanation Methodology
Individual case explanations were generated using `shap.TreeExplainer` against the exact transformed input space. Six representative cases were selected from the 2016 Test cohort to examine the specific attribution waterfalls.

## 4. Representative Test Cases
- **Case 348579 (High Risk / True Positive)**: Predicted Probability 0.91. Driven massively higher by complex specific `type_name`.
- **Case 319493 (Medium Risk)**: Predicted Probability 0.51. Conflicting push between `court_no` and fast `case_type`.
- **Case 326625 (Low Risk / True Negative)**: Predicted Probability 0.0006. Overwhelmingly driven to 0 by a highly efficient, fast-track case type (e.g. bail application).
- **Case 340843 (False Positive)**: Predicted Probability 0.87. Historically slow court caused a high score, but case resolved early (likely out-of-court settlement).
- **Case 346539 (False Negative)**: Predicted Probability 0.30. Expected to be fast, but stalled post-filing.

## 5. Interpretation Limitations
SHAP values define **model contribution** and **predictive association**, NOT causal effects. A specific judge ID having a high SHAP value means that cases assigned to that ID are historically delayed; it does NOT prove the judge caused the delay (which could be due to case allocation policy or geographical resource starvation).
