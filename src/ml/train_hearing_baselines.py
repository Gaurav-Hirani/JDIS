import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_and_split_hearing_data():
    df = pd.read_parquet("data/features/hearing_features.parquet")
    cases = pd.read_parquet("data/processed/cases_clean.parquet")
    
    # Merge to get exact date_last_list for temporal split
    df = df.merge(cases[['ddl_case_id', 'date_last_list_dt']], on='ddl_case_id', how='left')
    df['last_list_year'] = df['date_last_list_dt'].dt.year
    
    # 1. Target Filter: Remove missing and negative gaps
    df = df[df['next_listing_gap_days'].notna() & (df['next_listing_gap_days'] >= 0)]
    
    # 2. Chronological Split based on Prediction Point (last_list_year)
    train_df = df[df['last_list_year'] <= 2017].copy()
    val_df = df[df['last_list_year'] == 2018].copy()
    test_df = df[df['last_list_year'] == 2019].copy()
    
    # Identify Features
    target = 'next_listing_gap_days'
    exclude = [target, 'ddl_case_id', 'date_last_list_dt', 'last_list_year', 'filing_year', 'hearing_continuation_risk']
    features = [c for c in df.columns if c not in exclude]
    
    # Separate cat and num
    cat_cols = ['state_code', 'dist_code', 'court_no', 'state_str', 'district_str', 'court_str', 
                'case_type_str', 'case_category', 'is_criminal_code', 'purpose_str', 'judge_position_clean']
    # Ensure all cat_cols actually exist in features
    cat_cols = [c for c in cat_cols if c in features]
    num_cols = [c for c in features if c not in cat_cols]
    
    return train_df, val_df, test_df, features, num_cols, cat_cols

def build_preprocessor(num_cols, cat_cols):
    numeric_transformer = SimpleImputer(strategy='median')
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ]
    )
    return preprocessor

def evaluate_model(name, model, X_val, y_val):
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    r2 = r2_score(y_val, preds)
    return {'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2}

def main():
    os.makedirs("research/results", exist_ok=True)
    
    print("Loading data...")
    train_df, val_df, test_df, features, num_cols, cat_cols = load_and_split_hearing_data()
    
    X_train = train_df[features]
    X_train[cat_cols] = X_train[cat_cols].astype(str)
    y_train = train_df['next_listing_gap_days']
    
    X_val = val_df[features]
    X_val[cat_cols] = X_val[cat_cols].astype(str)
    y_val = val_df['next_listing_gap_days']
    
    preprocessor = build_preprocessor(num_cols, cat_cols)
    
    models = {
        'Mean Baseline': DummyRegressor(strategy='mean'),
        'Median Baseline': DummyRegressor(strategy='median'),
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10)
    }
    
    results = []
    
    for name, reg in models.items():
        print(f"Training {name}...")
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', reg)])
        pipe.fit(X_train, y_train)
        
        metrics = evaluate_model(name, pipe, X_val, y_val)
        results.append(metrics)
        print(f"{name} Validation -> MAE: {metrics['MAE']:.2f}, RMSE: {metrics['RMSE']:.2f}, R2: {metrics['R2']:.4f}")
        
    df_results = pd.DataFrame(results)
    df_results.to_csv("research/results/hearing_regression_baselines.csv", index=False)
    print("Baseline regression complete and saved.")

if __name__ == "__main__":
    main()
