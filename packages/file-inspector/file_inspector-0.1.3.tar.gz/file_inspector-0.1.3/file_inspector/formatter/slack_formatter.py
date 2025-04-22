# slack_formatter.py

from typing import Dict
import pandas as pd

from file_inspector.types import FileMetaInfo


def format_file_info(info: FileMetaInfo) -> str:
    return (
        f"📂 *파일 정보*\n"
        f"- 이름: `{info.file_name}`\n"
        f"- 경로: `{info.file_path}`\n"
        f"- 확장자: `{info.extension}`\n"
        f"- 크기: `{info.file_size}` bytes\n"
        f"- 인코딩: `{info.encoding}`\n"
        f"- 구분자: `{info.delimiter}`\n"
        f"- MIME 타입: `{info.mime_type}`\n"
        f"- 확인일: `{info.confirm_at}`\n"
        f"- 생성일: `{info.created_at}`\n"
        f"- 수정일: `{info.modified_at}`\n"
        f"- 압축 여부: {'✅' if info.is_compressed else '❌'}\n"
    )


def format_df_info(df: pd.DataFrame) -> str:
    return (
        f"📊 *데이터프레임 정보*\n"
        f"- 행 개수: `{df.shape[0]}`\n"
        f"- 열 개수: `{df.shape[1]}`\n"
        f"- 열 목록: `{', '.join(df.columns)}`\n"
    )


def format_slack_message(file_info: FileMetaInfo, df: pd.DataFrame) -> str:
    sections = []
    if file_info:
        sections.append(format_file_info(file_info))
    if df is not None:
        sections.append(format_df_info(df))
    return "\n".join(sections)
