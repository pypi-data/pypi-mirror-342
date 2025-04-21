# tests/test_inspector.py

import os
import unittest
from file_inspector import FileInspector
import pandas as pd

class TestFileInspector(unittest.TestCase):

    def setUp(self):
        self.inspector = FileInspector()
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        self.sample_file_path = os.path.join(self.data_dir, "sample.csv")

    def test_inspect_file(self):
        result = self.inspector.inspect(self.sample_file_path)
        self.assertTrue(result.file_info["file_exists"])
        self.assertIsInstance(result.df, pd.DataFrame)
        self.assertGreater(result.df.shape[0], 0)
        self.assertIn("file_name", result.file_info)
        self.assertIn("encoding", result.file_info)

    def test_inspect_file_schema_validation(self):
        result = self.inspector.inspect(self.sample_file_path)
        self.assertTrue(result.validate_schema(["id", "name", "value"]))
        self.assertFalse(result.validate_schema(["nonexistent_column"]))

    def test_inspect_sample_preview_and_summary(self):
        result = self.inspector.inspect(self.sample_file_path)
        preview = result.sample_preview(n=2)
        self.assertEqual(preview.shape[0], 2)
        summary = result.generate_summary_report()
        self.assertIn("value", summary.columns)

    def test_batch_inspect(self):
        results = self.inspector.batch_inspect(self.data_dir)
        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertTrue("file_path" in result.file_info)

if __name__ == "__main__":
    unittest.main()