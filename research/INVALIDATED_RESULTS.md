# Invalidated JDIS Experiments

This registry explicitly records outdated or methodologically flawed experiments that must **NOT** be used, reported, or cited in the final IEEE research paper.

---

### 1. Initial 2017 Filing-Time Classification Baseline
- **Date/Version**: Phase 1 / Early Phase 2
- **Experiment Description**: Classification baselines trained on all data up to 2016 and evaluated on the 2017 filing cohort.
- **Reason for Invalidation**: **Right-Censoring & Selection Bias**. The 2017 cohort evaluation incorrectly labeled unresolved cases as "on-time" (Label 0) if they hadn't crossed the 24-month threshold by the snapshot date, contaminating the target logic and causing massive evaluation bias. 
- **Replacement Experiment**: The "Final Filing-Time 24-Month Delay Classification (Phase 5)" which isolates true observed outcomes using the strictly defined 2010–2014 Train / 2015 Val / 2016 Test methodology.

---

### 2. Adjournment Prediction Task
- **Date/Version**: Early Phase 6 Scope
- **Experiment Description**: Attempts to predict formal judicial adjournments.
- **Reason for Invalidation**: **Lack of Label Validity**. The DDL public dataset aggregates case milestones and does not provide session-by-session procedural logs (e.g., formal Order XVII CPC adjournments).
- **Replacement Experiment**: Reframed to "Hearing Continuation & Next-Listing Delay Prediction," which correctly reflects the scheduling latency between chronological hearing dates.

---

### 3. NLP & Graph Network Classification (Phase 4 Additions)
- **Date/Version**: Phase 4 Feature Ablation
- **Experiment Description**: Models utilizing TF-IDF representations of case histories and complex judge mobility networks.
- **Reason for Invalidation**: **Empirical Non-Performance**. These features failed to provide a robust performance uplift on the validation set over the simpler "Config D" feature set, introducing unnecessary latency and complexity without predictive value.
- **Replacement Experiment**: Final model relies exclusively on the 29-feature Config D.
