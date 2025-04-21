# tests/test_inspector.py

import os
import unittest
from file_inspector import FileInspector

class TestFileInspector(unittest.TestCase):

    def setUp(self):
        self.file_path = os.path.join("data", "sample.csv")
        self.inspector = FileInspector()

    def test_inspect_basic(self):
        result = self.inspector.inspect(self.file_path)
        self.assertTrue(result.file_info["file_exists"])
        self.assertIsNotNone(result.df)
        self.assertGreater(result.df.shape[0], 0)

    def test_batch_inspect(self):
        results = self.inspector.batch_inspect("data")
        self.assertIsInstance(results, list)
        self.assertTrue(any(r.file_info["file_path"] == self.file_path for r in results))

if __name__ == "__main__":
    unittest.main()
