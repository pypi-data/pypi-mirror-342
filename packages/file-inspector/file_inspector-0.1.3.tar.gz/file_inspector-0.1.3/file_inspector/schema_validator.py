# schema_validator.py

import pandas as pd
from typing import List

class SchemaValidator:
    """
    DataFrame의 스키마(컬럼 구조)를 검증하는 클래스.
    단일 책임 원칙(SRP)에 따라 유효성 검증 기능만 담당.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def has_columns(self, required_columns: List[str]) -> bool:
        """
        DataFrame이 모든 필수 컬럼을 포함하는지 확인
        """
        return all(col in self.df.columns for col in required_columns)

    def missing_columns(self, required_columns: List[str]) -> List[str]:
        """
        누락된 컬럼 목록 반환
        """
        return [col for col in required_columns if col not in self.df.columns]
