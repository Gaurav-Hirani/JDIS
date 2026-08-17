"""
JDIS 4-Category Civil vs Criminal Classification Tests
"""

import unittest
from src.data.classify_case_type import classify_case_type_string, classify_case_record


class TestClassification(unittest.TestCase):

    def test_criminal_classification_rules(self):
        self.assertEqual(classify_case_type_string("cc"), "Criminal")
        self.assertEqual(classify_case_type_string("cri. case"), "Criminal")
        self.assertEqual(classify_case_type_string("sessions trial"), "Criminal")
        self.assertEqual(classify_case_type_string("bail application"), "Criminal")
        self.assertEqual(classify_case_type_string("138 ni act"), "Criminal")
        
        self.assertEqual(classify_case_record("Criminal", act_id=17353), "High-Confidence Criminal")
        self.assertEqual(classify_case_record("Other/Unknown/Unclassified", act_id=17353), "High-Confidence Criminal")

    def test_civil_classification_rules(self):
        self.assertEqual(classify_case_type_string("original suit"), "Civil")
        self.assertEqual(classify_case_type_string("os"), "Civil")
        self.assertEqual(classify_case_type_string("mact"), "Civil")
        self.assertEqual(classify_case_type_string("execution petition"), "Civil")
        self.assertEqual(classify_case_type_string("hindu marriage act petition"), "Civil")
        
        self.assertEqual(classify_case_record("Civil", act_id=4747), "High-Confidence Civil")
        self.assertEqual(classify_case_record("Other/Unknown/Unclassified", act_id=7276), "High-Confidence Civil")

    def test_ambiguous_and_unknown_rules(self):
        # Conflict between Civil type and Criminal Act
        self.assertEqual(classify_case_record("Civil", act_id=17353), "Ambiguous/Mixed")
        self.assertEqual(classify_case_record("Criminal", act_id=4747), "Ambiguous/Mixed")
        
        # Completely unknown type and unknown Act
        self.assertEqual(classify_case_record("Other/Unknown/Unclassified", act_id=999999), "Other/Unknown/Unclassified")


if __name__ == '__main__':
    unittest.main()
