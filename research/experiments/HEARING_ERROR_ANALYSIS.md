# Hearing Next-Listing Delay: Error Analysis

## 1. Regression Performance
The defining conclusion of the Phase 6 error analysis is that under the evaluated feature set and models, exact next-listing delay did not achieve useful out-of-time predictive performance at the prediction point $T_{\text{last\_list}}$.

Across all tested models (Linear, Trees, Random Forest, XGBoost), the out-of-sample (2019) R² score is **negative**. A negative R² indicates that the trained ML regressors perform systematically *worse* than simply predicting the historical dataset mean.

## 2. Structural Drivers of Error
By breaking down the errors into Gap Buckets, we identify the primary failure modes:

1. **The Same-Day Mode (0 Days)**
   - Over 40% of the dataset consists of zero-day gaps (where cases are formally recorded as continuing on the same day or without a break).
   - Because regressors try to minimize global MSE across the entire continuous scale, they severely overpredict these 0-day gaps.

2. **The Long-Tail Variance (>60 Days)**
   - When actual gaps extend beyond 2 months, the model systematically underpredicts them.
   - The Random Forest predicts an "average" moderate delay to hedge its loss, resulting in massive underestimations for cases that genuinely get adjourned for 3-6 months.

## 3. Subgroup Stability
The error magnitude is structurally consistent across subgroups (States, Judge Positions). There is no "hidden pocket" of high predictability. The lack of signal is systemic across the available variables, not localized to a specific court type.

## 4. Conclusion
Unobserved operational variables—such as lawyer scheduling conflicts, judge administrative leave, or daily courtroom diary limits—likely contribute to the difficulty of predicting the exact gap. However, this does not establish that next-listing delay is inherently unpredictable; it establishes the limitation of the available data/features and tested models.
