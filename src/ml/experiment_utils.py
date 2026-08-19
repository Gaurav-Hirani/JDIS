import os
import time
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix,
                             roc_curve, precision_recall_curve)

def register_experiment(exp_id, objective, dataset, target, model_name, val_protocol, metric_result):
    """Appends an experiment record to EXPERIMENT_REGISTER.md"""
    reg_path = "research/experiments/EXPERIMENT_REGISTER.md"
    date_str = time.strftime("%Y-%m-%d")
    
    record = f"| {exp_id} | {date_str} | {objective} | {dataset} | {target} | {model_name} | {val_protocol} | {metric_result} | Saved |\n"
    
    if not os.path.exists(reg_path):
        os.makedirs(os.path.dirname(reg_path), exist_ok=True)
        with open(reg_path, "w") as f:
            f.write("# JDIS ML Experiment Register\n\n")
            f.write("| Experiment ID | Date | Objective | Dataset | Target | Model | Validation Protocol | Key Metric | Result |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            
    with open(reg_path, "a") as f:
        f.write(record)

def plot_regression_results(y_true, y_pred, exp_id, model_name):
    """Generates actual vs predicted and residual distribution plots"""
    os.makedirs("research/figures", exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Actual vs Predicted
    axes[0].scatter(y_true, y_pred, alpha=0.1)
    axes[0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    axes[0].set_xlabel("Actual Duration (Days)")
    axes[0].set_ylabel("Predicted Duration (Days)")
    axes[0].set_title(f"{model_name}: Actual vs Predicted")
    
    # Residuals
    residuals = y_true - y_pred
    sns.histplot(residuals, bins=50, ax=axes[1])
    axes[1].set_xlabel("Residuals (Actual - Predicted)")
    axes[1].set_title(f"{model_name}: Residuals")
    
    plt.tight_layout()
    plt.savefig(f"research/figures/{exp_id}_regression_plots.png")
    plt.close()

def plot_classification_results(y_true, y_pred, y_prob, exp_id, model_name):
    """Generates confusion matrix, ROC curve, and PR curve"""
    os.makedirs("research/figures", exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0])
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")
    axes[0].set_title(f"{model_name}: Confusion Matrix")
    
    # ROC Curve
    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        axes[1].plot(fpr, tpr, label=f"AUC = {auc:.3f}")
        axes[1].plot([0, 1], [0, 1], 'r--')
        axes[1].set_xlabel("FPR")
        axes[1].set_ylabel("TPR")
        axes[1].set_title(f"{model_name}: ROC Curve")
        axes[1].legend()
        
        # PR Curve
        prec, rec, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = average_precision_score(y_true, y_prob)
        axes[2].plot(rec, prec, label=f"PR-AUC = {pr_auc:.3f}")
        axes[2].set_xlabel("Recall")
        axes[2].set_ylabel("Precision")
        axes[2].set_title(f"{model_name}: PR Curve")
        axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(f"research/figures/{exp_id}_classification_plots.png")
    plt.close()

def evaluate_regression(model, X_val, y_val, exp_id, model_name):
    y_pred = model.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    r2 = r2_score(y_val, y_pred)
    
    plot_regression_results(y_val, y_pred, exp_id, model_name)
    
    return {"MAE": mae, "RMSE": rmse, "R2": r2}

def evaluate_classification(model, X_val, y_val, exp_id, model_name):
    y_pred = model.predict(X_val)
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_val)[:, 1]
    else:
        y_prob = None
        
    acc = accuracy_score(y_val, y_pred)
    # Handle zero division warning for precision
    prec = precision_score(y_val, y_pred, zero_division=0)
    rec = recall_score(y_val, y_pred, zero_division=0)
    f1 = f1_score(y_val, y_pred, zero_division=0)
    
    roc_auc = roc_auc_score(y_val, y_prob) if y_prob is not None else np.nan
    pr_auc = average_precision_score(y_val, y_prob) if y_prob is not None else np.nan
    
    plot_classification_results(y_val, y_pred, y_prob, exp_id, model_name)
    
    return {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1, "ROC-AUC": roc_auc, "PR-AUC": pr_auc}

def check_data_validity(df, feature_cols, target_col):
    """Checks for NaNs in features and target existence"""
    if target_col not in df.columns:
        raise ValueError(f"Target column {target_col} missing from dataset.")
        
    for col in feature_cols:
        if df[col].isna().sum() > 0:
            print(f"Warning: {col} has {df[col].isna().sum()} missing values. Preprocessing will handle it.")
            
    # Check for leakage
    leakage_cols = ['date_of_decision', 'disp_name', 'ddl_decision_judge_id', 'date_next_list']
    for leak in leakage_cols:
        if leak in feature_cols:
            raise ValueError(f"CRITICAL: Leakage column {leak} found in features!")

