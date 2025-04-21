# tests/test_file_reader.py

import os
import unittest
import pandas as pd
from file_inspector.file_reader import FileReader

class TestFileReader(unittest.TestCase):

    def setUp(self):
        self.file_reader = FileReader()
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

        self.sample_files = {
            "csv": {
                "file_path": os.path.join(self.base_dir, "sample.csv"),
                "file_extension": ".csv",
                "encoding": "utf-8",
                "delimiter": ","
            },
            "tsv": {
                "file_path": os.path.join(self.base_dir, "sample.tsv"),
                "file_extension": ".tsv",
                "encoding": "utf-8",
                "delimiter": "\t"
            },
            "xlsx": {
                "file_path": os.path.join(self.base_dir, "sample.xlsx"),
                "file_extension": ".xlsx",
                "encoding": None,
                "delimiter": None
            },
            "json": {
                "file_path": os.path.join(self.base_dir, "sample.json"),
                "file_extension": ".json",
                "encoding": "utf-8",
                "delimiter": None
            },
            # "parquet": {
            #     "file_path": os.path.join(self.base_dir, "sample.parquet"),
            #     "file_extension": ".parquet",
            #     "encoding": None,
            #     "delimiter": None
            # }
        }

    def test_various_supported_formats(self):
        for filetype, fileinfo in self.sample_files.items():
            with self.subTest(filetype=filetype):
                file_info = {"file_exists": True, **fileinfo}
                df = self.file_reader.read(file_info)
                self.assertIsInstance(df, pd.DataFrame)
                self.assertGreater(df.shape[0], 0)
                self.assertGreater(df.shape[1], 0)

    def test_read_with_invalid_extension(self):
        invalid_ext_info = {"file_exists": True, "file_path": os.path.join(self.base_dir, "sample.exe"), "file_extension": ".exe", "encoding": "utf-8", "delimiter": ","}
        df = self.file_reader.read(invalid_ext_info)
        self.assertIsNone(df)

    def test_read_with_file_does_not_exist_flag(self):
        info = {**self.sample_files["csv"], "file_exists": False}
        df = self.file_reader.read(info)
        self.assertIsNone(df)

    def test_read_nonexistent_path(self):
        info = {**self.sample_files["csv"], "file_exists": True, "file_path": "not_found.csv"}
        df = self.file_reader.read(info)
        self.assertIsNone(df)

    def test_read_empty_csv(self):
        empty_file = os.path.join(self.base_dir, "empty.csv")
        with open(empty_file, "w") as f:
            f.write("")
        info = {"file_exists": True, "file_path": empty_file, "file_extension": ".csv", "encoding": "utf-8", "delimiter": ","}
        df = self.file_reader.read(info)
        self.assertIsNone(df)
        os.remove(empty_file)

if __name__ == "__main__":
    unittest.main()
