"""
JDIS NLP & TF-IDF Feature Engineering Module
Builds composite legal metadata text strings, fits TF-IDF vectorizer
strictly on the training cohort (2010-2016), and applies TruncatedSVD dimensionality reduction.
"""

import pandas as pd
import numpy as np
import os
import joblib
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

logger = logging.getLogger(__name__)


def build_composite_text_series(df: pd.DataFrame) -> pd.Series:
    """
    Constructs a composite legal text representation per case using filing-time metadata.
    """
    text_series = (
        df['state_str'].fillna('') + " " +
        df['district_str'].fillna('') + " " +
        df['court_str'].fillna('') + " " +
        df['case_type_str'].fillna('') + " " +
        df['case_category'].fillna('') + " " +
        df['judge_position_clean'].fillna('')
    ).str.lower().str.replace(r'[^\w\s]', ' ', regex=True)
    return text_series


def generate_tfidf_features(df: pd.DataFrame, 
                            train_mask: pd.Series, 
                            n_components: int = 50,
                            artifacts_dir: str = 'data/features') -> pd.DataFrame:
    """
    Fits TF-IDF vectorizer + TruncatedSVD strictly on the training partition (train_mask == True)
    and transforms the entire dataset.
    
    Saves artifacts for deployment / inference reproducibility.
    """
    logger.info(f"Generating TF-IDF features with {n_components} SVD components...")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    text_corpus = build_composite_text_series(df)
    train_corpus = text_corpus[train_mask]
    
    logger.info(f"Fitting TfidfVectorizer on {len(train_corpus):,} training documents...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=5,
        stop_words='english'
    )
    X_train_tfidf = vectorizer.fit_transform(train_corpus)
    
    logger.info(f"Fitting TruncatedSVD({n_components}) on training TF-IDF matrix...")
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    svd.fit(X_train_tfidf)
    
    # Save artifacts
    joblib.dump(vectorizer, os.path.join(artifacts_dir, 'tfidf_vectorizer.joblib'))
    joblib.dump(svd, os.path.join(artifacts_dir, 'tfidf_svd_model.joblib'))
    logger.info(f"Saved TF-IDF models to {artifacts_dir}.")
    
    # Transform entire corpus
    logger.info("Transforming full corpus with fitted TF-IDF + SVD...")
    X_all_tfidf = vectorizer.transform(text_corpus)
    X_all_svd = svd.transform(X_all_tfidf)
    
    svd_cols = [f"tfidf_{i}" for i in range(n_components)]
    svd_df = pd.DataFrame(X_all_svd, columns=svd_cols, index=df.index)
    
    return svd_df
