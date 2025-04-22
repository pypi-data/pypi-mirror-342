# file_inspector/file_reader.py

import pandas as pd
from typing import Optional, Dict

from file_inspector.types import IFileReader, FileMetaInfo


class FileReader(IFileReader):
    """
    📂 파일 확장자에 따라 pandas DataFrame으로 파일을 읽어오는 클래스.
    ✅ 단일 책임 원칙(SRP)에 따라 파일 로딩만 담당.
    """

    def read(self, file_info: FileMetaInfo) -> Optional[pd.DataFrame]:
        if not file_info.file_exists:
            print(f"[FileReader] 파일 없음: {file_info.file_path}")
            return None

        extension = file_info.extension
        path = file_info.file_path
        encoding = file_info.encoding
        delimiter = file_info.delimiter

        try:
            if extension in ['.csv', '.txt', '.tsv']:
                return pd.read_csv(path, encoding=encoding, delimiter=delimiter)
            elif extension in ['.xls', '.xlsx']:
                return pd.read_excel(path)
            elif extension == '.json':
                return pd.read_json(path)
            elif extension == '.parquet':
                return pd.read_parquet(path)
            else:
                print(f"[FileReader] 지원하지 않는 확장자: {extension}")
        except Exception as e:
            print(f"[FileReader Error] {e}")

        return None
