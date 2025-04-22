# types.py

from typing import Protocol, Dict, Optional
import pandas as pd
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileMetaInfo:
    file_exists: bool
    file_path: str
    confirm_at: datetime
    message: Optional[str] = None
    file_name: Optional[str] = None
    extension: Optional[str] = None
    file_size: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    mime_type: Optional[str] = None
    encoding: Optional[str] = None
    delimiter: Optional[str] = None
    is_compressed: Optional[bool] = None

class IFileReader(Protocol):
    def read(self, file_info: FileMetaInfo) -> Optional[pd.DataFrame]:
        ...


class IFileInfoExtractor(Protocol):
    def extract(self, file_path: str) -> FileMetaInfo:
        ...


class ISchemaValidator(Protocol):
    def has_columns(self, required_columns: list[str]) -> bool:
        ...

    def missing_columns(self, required_columns: list[str]) -> list[str]:
        ...
