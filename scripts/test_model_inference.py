import joblib
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("1. Loading Models...")
clf = joblib.load("models/final_calibrated_clf.joblib")
print("Calibrated Classifier Loaded Successfully:", type(clf))

reg = joblib.load("models/best_ablation_reg.joblib")
print("Regressor Loaded Successfully:", type(reg))

# Test sample input
sample_data = {
    'filing_month': [5],
    'filing_day_of_week': [2],
    'filing_quarter': [2],
    'type_name': ['criminal appeal'],
    'case_type_str': ['criminal'],
    'case_category': ['criminal'],
    'is_criminal_code': [1],
    'statutory_act_count': [1],
    'ipc_section_count': [2],
    'bailable_ipc_flag': ['bailable'],
    'primary_act_id': ['act_ipc'],
    'female_defendant_clean': ['0'],
    'female_petitioner_clean': ['0'],
    'female_adv_def_clean': ['0'],
    'female_adv_pet_clean': ['0'],
    'state_code': ['01'],
    'dist_code': ['01'],
    'court_no': ['01'],
    'state_str': ['Maharashtra'],
    'district_str': ['Mumbai'],
    'court_str': ['Chief Metropolitan Magistrate'],
    'ddl_filing_judge_id': ['judge_101'],
    'judge_position_clean': ['magistrate'],
    'judge_gender': ['male'],
    'judge_tenure_days': [500.0],
    'court_prior_delay_rate': [0.45],
    'court_prior_avg_duration': [650.0],
    'court_prior_active_backlog': [1200.0],
    'casetype_prior_delay_rate': [0.38]
}

df = pd.DataFrame(sample_data)
print("2. Running Classifier Prediction...")
clf_prob = clf.predict_proba(df)[:, 1]
print(f"Calibrated Delay Probability: {clf_prob[0]:.4f}")

risk_score = int(np.floor(clf_prob[0] * 100))
print(f"JDIS Risk Score: {risk_score}")

def get_risk_band(score):
    if score <= 20:
        return "Low"
    elif score <= 50:
        return "Moderate"
    elif score <= 80:
        return "High"
    else:
        return "Very High"

print(f"Risk Band: {get_risk_band(risk_score)}")

print("3. Running Regressor Prediction...")
reg_pred = reg.predict(df)
print(f"Predicted Case Duration Days: {reg_pred[0]:.2f}")

print("4. Inspecting Base Pipeline for SHAP...")
# In CalibratedClassifierCV, let's see how the base pipeline is stored
if hasattr(clf, "estimator"):
    base_pipe = clf.estimator
    if hasattr(base_pipe, "estimator"):
        base_pipe = base_pipe.estimator
elif hasattr(clf, "calibrated_classifiers_"):
    base_pipe = clf.calibrated_classifiers_[0].estimator
    if hasattr(base_pipe, "estimator"):
        base_pipe = base_pipe.estimator
else:
    base_pipe = None

print("Base Pipeline Extracted:", type(base_pipe))
if hasattr(base_pipe, "named_steps"):
    print("Base Pipeline Steps:", list(base_pipe.named_steps.keys()))
    preprocessor = base_pipe.named_steps['preprocessor']
    model = base_pipe.named_steps['model']
    print("Preprocessor:", type(preprocessor))
    print("Model:", type(model))

    import shap
    X_trans = preprocessor.transform(df)
    feature_names = preprocessor.get_feature_names_out()
    feature_names = [f.replace('num__', '').replace('cat__', '') for f in feature_names]
    X_dense = X_trans.toarray() if hasattr(X_trans, 'toarray') else X_trans
    X_df = pd.DataFrame(X_dense, columns=feature_names)
    
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X_df)
    print("SHAP Values shape:", np.array(shap_vals).shape)
    print("SHAP Base Value:", explainer.expected_value)
    
    # Top 5 features
    top_indices = np.argsort(np.abs(shap_vals[0]))[-5:][::-1]
    print("Top 5 SHAP features for sample:")
    for idx in top_indices:
        print(f"  - {feature_names[idx]}: {shap_vals[0][idx]:.4f} (val: {X_df.iloc[0, idx]})")

print("\n=== ALL INFERENCE & SHAP CHECKS PASSED ===")
