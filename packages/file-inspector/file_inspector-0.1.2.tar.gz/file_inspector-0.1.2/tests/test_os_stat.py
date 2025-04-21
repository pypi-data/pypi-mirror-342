import os
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        file_path = r"C:\Users\user\Downloads\kb_naver_kakao_category_2025_04_workset_org_202503.csv"
        stat = os.stat(file_path)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
