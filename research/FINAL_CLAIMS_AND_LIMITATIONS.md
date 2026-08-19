# Final Claims and Limitations

To maintain strict scientific and methodological integrity, the following boundaries must be adhered to when writing the final research paper or presenting the tool.

## 1. Directly Demonstrated Findings
We can explicitly claim:
- **Calibrated Prediction**: Machine learning models can differentiate filing-time risk of severe case delay with high discrimination (ROC-AUC ~0.79) using entirely structured metadata available at filing.
- **Isotonic Reliability**: Applying Isotonic Regression strictly aligns predicted probabilities with true empirical event frequencies.
- **Categorical Dominance**: Structural factors like specific Case Types (`type_name`) and Geographic Assignments (`court_no`) hold the highest predictive associations.
- **Negative Predictability (Duration & Scheduling)**: Predicting the exact day-level duration of a case, or the exact scheduling gap of a next-listing, yields negative out-of-time R² under standard algorithms and features.

## 2. Reasonable Interpretations
We can reasonably interpret (but not definitively prove) that:
- Structural backlogs and operational differences between local courts exert a massive systemic influence over case length.
- The inability to predict next-listing scheduling latency is likely driven by unobserved, micro-temporal daily operational constraints (such as sudden lawyer unavailability or specific courtroom diary limits).

## 3. Claims We Must NOT Make
Under no circumstances should the research paper claim:
- **Causal Effects**: E.g., "Judge X causes a 400-day delay." The model finds *associations*, which may be confounded by non-random case allocation.
- **Unsupported Statistical-Significance Claims**: E.g., "The model is statistically significantly better." We did not perform bootstrapped significance testing on the test fold. Use "observed out-of-time improvement."
- **State of the Art / First Ever**: Unless exhaustively proven by a comprehensive systematic literature review.
- **Structurally Impossible**: For Dataset C (Hearing Prediction). We must state that the *tested features* were insufficient, rather than claiming that the fundamental problem is completely unsolvable under any hypothetical data collection paradigm.
- **Adjournment Prediction**: Do not claim the system predicts adjournments. It predicts *scheduling latency* between dates.
