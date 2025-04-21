# tests/test_validators.py

import unittest
import pandas as pd
from file_inspector.schema_validator import SchemaValidator

class TestSchemaValidator(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [10.5, 20.1, 30.6]
        })
        self.validator = SchemaValidator(self.df)

    def test_has_columns_all_exist(self):
        self.assertTrue(self.validator.has_columns(["id", "name"]))

    def test_has_columns_some_missing(self):
        self.assertFalse(self.validator.has_columns(["id", "unknown"]))

    def test_missing_columns(self):
        missing = self.validator.missing_columns(["id", "value", "age"])
        self.assertEqual(missing, ["age"])

    def test_missing_columns_all_present(self):
        missing = self.validator.missing_columns(["id", "name", "value"])
        self.assertEqual(missing, [])

if __name__ == "__main__":
    unittest.main()