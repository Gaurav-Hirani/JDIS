| Task           | Type     | Model               |   Accuracy |   Precision |     Recall |         F1 |    ROC-AUC |     PR-AUC |     MAE |    RMSE |         R2 |
|:---------------|:---------|:--------------------|-----------:|------------:|-----------:|-----------:|-----------:|-----------:|--------:|--------:|-----------:|
| Classification | Baseline | Logistic Regression |   0.709628 |    0.625357 |   0.350839 |   0.449499 |   0.725807 |   0.561001 | nan     | nan     | nan        |
| Classification | Advanced | XGBoost Classifier  |   0.734383 |    0.672234 |   0.417462 |   0.515065 |   0.782629 |   0.62777  | nan     | nan     | nan        |
| Regression     | Baseline | Linear Regression   | nan        |  nan        | nan        | nan        | nan        | nan        | 346.708 | 430.618 |  -0.922161 |
| Regression     | Advanced | XGBoost Regressor   | nan        |  nan        | nan        | nan        | nan        | nan        | 261.653 | 326.7   |  -0.106378 |