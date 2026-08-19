import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score, precision_recall_curve, auc

def expected_calibration_error(y_true, y_prob, n_bins=10):
    bins = np.linspace(0., 1., n_bins + 1)
    binids = np.digitize(y_prob, bins) - 1
    
    ece = 0.0
    for i in range(n_bins):
        mask = binids == i
        if np.any(mask):
            prob_true = np.mean(y_true[mask])
            prob_pred = np.mean(y_prob[mask])
            abs_diff = np.abs(prob_true - prob_pred)
            ece += (np.sum(mask) / len(y_prob)) * abs_diff
    return ece

def calculate_pr_auc(y_true, y_prob):
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    return auc(recall, precision)

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures", exist_ok=True)
    
    print("Loading data and model...")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    val_mask = df_clf['filing_year'] == 2015
    test_mask = df_clf['filing_year'] == 2016
    
    df_val = df_clf[val_mask].copy()
    df_test = df_clf[test_mask].copy()
    
    pipe = joblib.load("models/best_ablation_clf.joblib")
    preprocessor = pipe.named_steps['preprocessor']
    
    num_cols = preprocessor.transformers_[0][2]
    cat_cols = preprocessor.transformers_[1][2]
    features = num_cols + cat_cols
    
    X_val = df_val[features].copy()
    X_val[cat_cols] = X_val[cat_cols].astype(str)
    y_val = df_val['delay_24m'].values
    
    X_test = df_test[features].copy()
    X_test[cat_cols] = X_test[cat_cols].astype(str)
    y_test = df_test['delay_24m'].values
    
    # ---------------------------------------------------------
    # PHASE 5D: CALIBRATION ON VALIDATION SET
    # ---------------------------------------------------------
    print("Evaluating calibration methods on 2015 Validation...")
    
    y_prob_uncal = pipe.predict_proba(X_val)[:, 1]
    
    from sklearn.frozen import FrozenEstimator
    
    # Fit Sigmoid (Platt)
    cal_sigmoid = CalibratedClassifierCV(estimator=FrozenEstimator(pipe), method='sigmoid')
    cal_sigmoid.fit(X_val, y_val)
    y_prob_sig = cal_sigmoid.predict_proba(X_val)[:, 1]
    
    # Fit Isotonic
    cal_isotonic = CalibratedClassifierCV(estimator=FrozenEstimator(pipe), method='isotonic')
    cal_isotonic.fit(X_val, y_val)
    y_prob_iso = cal_isotonic.predict_proba(X_val)[:, 1]
    
    methods = {
        'Uncalibrated XGBoost': y_prob_uncal,
        'Platt (Sigmoid) Scaling': y_prob_sig,
        'Isotonic Regression': y_prob_iso
    }
    
    val_results = []
    
    plt.figure(figsize=(10, 8))
    plt.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    
    best_brier = float('inf')
    best_cal_name = None
    best_cal_model = None
    
    for name, probs in methods.items():
        brier = brier_score_loss(y_val, probs)
        ll = log_loss(y_val, probs)
        ece = expected_calibration_error(y_val, probs, n_bins=15)
        
        val_results.append({
            'Calibration_Method': name,
            'Brier_Score': brier,
            'Log_Loss': ll,
            'ECE': ece
        })
        
        # Plotting curve
        prob_true, prob_pred = calibration_curve(y_val, probs, n_bins=10)
        plt.plot(prob_pred, prob_true, marker='s', label=f"{name} (ECE: {ece:.3f})")
        
        # Select best calibrator based on Brier Score
        if brier < best_brier:
            best_brier = brier
            best_cal_name = name
            if name == 'Platt (Sigmoid) Scaling':
                best_cal_model = cal_sigmoid
            elif name == 'Isotonic Regression':
                best_cal_model = cal_isotonic
            else:
                best_cal_model = pipe # Uncalibrated
                
    pd.DataFrame(val_results).to_csv("research/results/calibration_validation.csv", index=False)
    
    plt.ylabel("Fraction of positives (True)")
    plt.xlabel("Mean predicted probability")
    plt.title("Calibration Curves (2015 Validation)")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("research/figures/calibration_curve_validation.png", bbox_inches='tight')
    plt.close()
    
    print(f"Selected Best Calibration Method: {best_cal_name}")
    
    # Save the selected calibrator pipeline
    joblib.dump(best_cal_model, "models/final_calibrated_clf.joblib")
    
    # ---------------------------------------------------------
    # PHASE 5E: FINAL CALIBRATED TEST EVALUATION
    # ---------------------------------------------------------
    print("Evaluating best calibrator on 2016 Test cohort...")
    
    # We use best_cal_model
    y_prob_test = best_cal_model.predict_proba(X_test)[:, 1]
    
    test_brier = brier_score_loss(y_test, y_prob_test)
    test_ll = log_loss(y_test, y_prob_test)
    test_roc_auc = roc_auc_score(y_test, y_prob_test)
    test_pr_auc = calculate_pr_auc(y_test, y_prob_test)
    test_ece = expected_calibration_error(y_test, y_prob_test, n_bins=15)
    
    test_results = [{
        'Calibration_Method': best_cal_name,
        'Brier_Score': test_brier,
        'Log_Loss': test_ll,
        'ECE': test_ece,
        'ROC-AUC': test_roc_auc,
        'PR-AUC': test_pr_auc
    }]
    
    pd.DataFrame(test_results).to_csv("research/results/calibration_test.csv", index=False)
    
    # Plot final test calibration
    plt.figure(figsize=(10, 8))
    plt.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    prob_true, prob_pred = calibration_curve(y_test, y_prob_test, n_bins=10)
    plt.plot(prob_pred, prob_true, marker='s', label=f"{best_cal_name} (ECE: {test_ece:.3f})")
    plt.ylabel("Fraction of positives (True)")
    plt.xlabel("Mean predicted probability")
    plt.title("Calibration Curve (2016 Test)")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("research/figures/calibration_curve_test.png", bbox_inches='tight')
    plt.close()
    
    print("Calibration analysis complete.")

if __name__ == "__main__":
    main()
