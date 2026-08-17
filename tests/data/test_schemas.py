"""
JDIS Schema & Data Integrity Tests
"""

import os
import unittest
import pandas as pd
import numpy as np


class TestSchemas(unittest.TestCase):

    def test_processed_cases_clean_exists(self):
        path = "data/processed/cases_clean.parquet"
        self.assertTrue(os.path.exists(path), f"Missing {path}")
        df = pd.read_parquet(path)
        self.assertGreater(len(df), 0, "Dataset is empty")
        self.assertIn("ddl_case_id", df.columns)
        self.assertIn("case_duration_days", df.columns)
        self.assertIn("delay_24m", df.columns)

    def test_dataset_a_filing_features_schema(self):
        path = "data/features/filing_features.parquet"
        self.assertTrue(os.path.exists(path), f"Missing {path}")
        df = pd.read_parquet(path)
        self.assertGreater(len(df), 0)
        
        expected_cols = [
            "ddl_case_id", "filing_year", "state_code", "dist_code", "court_no",
            "case_category", "is_criminal_code", "court_prior_delay_rate",
            "court_prior_avg_duration", "court_prior_active_backlog",
            "judge_court_degree", "judge_tenure_days", "tfidf_0", "tfidf_49",
            "case_duration_days", "delay_24m"
        ]
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Missing expected column {col} in Dataset A")

    def test_dataset_c_hearing_features_schema(self):
        path = "data/features/hearing_features.parquet"
        self.assertTrue(os.path.exists(path), f"Missing {path}")
        df = pd.read_parquet(path)
        self.assertIn("next_listing_gap_days", df.columns)
        self.assertIn("hearing_continuation_risk", df.columns)
        self.assertIn("hearing_span_days", df.columns)

    def test_no_negative_durations_in_resolved(self):
        path = "data/features/filing_features.parquet"
        df = pd.read_parquet(path)
        resolved = df[df["case_duration_days"].notna()]
        self.assertTrue((resolved["case_duration_days"] >= 0).all(), "Found negative case durations in resolved records!")


if __name__ == '__main__':
    unittest.main()
