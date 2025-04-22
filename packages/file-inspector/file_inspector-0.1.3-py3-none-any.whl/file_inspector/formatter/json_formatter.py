# json_formatter.py

from typing import Dict, Optional
import pandas as pd
import json

from file_inspector.types import FileMetaInfo


def format_file_info_json(info: FileMetaInfo) -> str:
    return json.dumps(info.__dict__, indent=2, default=str)


def format_df_info_json(df: Optional[pd.DataFrame]) -> str:
    if df is None:
        return json.dumps({"message": "No DataFrame available."})

    preview = df.head().to_dict(orient="records")
    summary = df.describe(include='all').to_dict()
    return json.dumps({
        "preview": preview,
        "summary": summary
    }, indent=2, default=str)


def format_json_report(file_info: FileMetaInfo, df: Optional[pd.DataFrame]) -> str:
    result = {
        "file_info": file_info.__dict__,
        "dataframe": {
            "shape": df.shape if df is not None else [0, 0],
            "columns": list(df.columns) if df is not None else [],
            "sample": df.head().to_dict(orient="records") if df is not None else [],
            "summary": df.describe(include='all').to_dict() if df is not None else {}
        }
    }
    return json.dumps(result, indent=2, default=str)
