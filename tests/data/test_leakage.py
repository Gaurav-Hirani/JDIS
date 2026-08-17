"""
JDIS Feature Leakage Prevention & Time-Safety Tests
"""

import os
import unittest
import pandas as pd
import numpy as np


class TestLeakage(unittest.TestCase):

    def test_zero_tier_c_columns_in_dataset_a(self):
        """
        Asserts that no post-disposition or future target-derived columns are present
        as features in Dataset A (Filing-Time Model).
        """
        path = "data/features/filing_features.parquet"
        df = pd.read_parquet(path)
        
        prohibited_features = [
            "date_of_decision", "date_of_decision_dt",
            "disp_name", "disp_str", "disp_name_s",
            "ddl_decision_judge_id",
            "date_first_list", "date_first_list_dt",
            "date_last_list", "date_last_list_dt",
            "date_next_list", "date_next_list_dt",
            "next_listing_gap_days", "hearing_span_days",
            "filing_to_first_list_days", "hearing_continuation_risk"
        ]
        
        for col in prohibited_features:
            self.assertNotIn(col, df.columns, f"LEAKAGE DETECTED: Prohibited column {col} found in Dataset A!")

    def test_zero_next_listing_date_in_dataset_c(self):
        """
        Asserts that date_next_list is not included in Dataset C (outcome to predict).
        """
        path = "data/features/hearing_features.parquet"
        df = pd.read_parquet(path)
        self.assertNotIn("date_next_list", df.columns)
        self.assertNotIn("date_next_list_dt", df.columns)

    def test_temporal_split_integrity(self):
        """
        Verifies that the temporal splits strictly follow:
        Train (<= 2016), Val (2017), Test (2018).
        """
        path = "data/features/filing_features.parquet"
        df = pd.read_parquet(path)
        
        train_years = df[df["filing_year"] <= 2016]["filing_year"].unique()
        val_years = df[df["filing_year"] == 2017]["filing_year"].unique()
        test_years = df[df["filing_year"] == 2018]["filing_year"].unique()
        
        self.assertTrue(set(train_years).issubset({2010, 2011, 2012, 2013, 2014, 2015, 2016}))
        self.assertEqual(list(val_years), [2017])
        self.assertEqual(list(test_years), [2018])


if __name__ == '__main__':
    unittest.main()
