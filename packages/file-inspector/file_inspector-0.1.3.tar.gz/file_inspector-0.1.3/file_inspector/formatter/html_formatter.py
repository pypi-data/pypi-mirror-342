# html_formatter.py

from typing import Dict
import pandas as pd

from file_inspector.types import FileMetaInfo


def format_file_info_html(info: FileMetaInfo) -> str:
    return f"""
    <h2>📂 파일 정보</h2>
    <ul>
        <li><strong>파일 이름</strong>: {info.file_name}</li>
        <li><strong>경로</strong>: {info.file_path}</li>
        <li><strong>확장자</strong>: {info.extension}</li>
        <li><strong>파일 크기</strong>: {info.file_size} bytes</li>
        <li><strong>인코딩</strong>: {info.encoding}</li>
        <li><strong>구분자</strong>: {info.delimiter}</li>
        <li><strong>MIME 타입</strong>: {info.mime_type}</li>
        <li><strong>확인일</strong>: {info.confirm_at}</li>
        <li><strong>생성일</strong>: {info.created_at}</li>
        <li><strong>수정일</strong>: {info.modified_at}</li>
        <li><strong>압축 여부</strong>: {'✅' if info.is_compressed else '❌'}</li>
    </ul>
    """


def format_df_info_html(df: pd.DataFrame) -> str:
    summary_html = df.describe(include='all').to_html() if df is not None else "<p>No summary available.</p>"
    return f"""
    <h2>📊 데이터프레임 정보</h2>
    <p><strong>행 개수:</strong> {df.shape[0]}<br>
    <strong>열 개수:</strong> {df.shape[1]}<br>
    <strong>열 목록:</strong> {', '.join(df.columns)}</p>
    <h3>기술 통계 요약</h3>
    {summary_html}
    """


def format_html_report(file_info: FileMetaInfo, df: pd.DataFrame) -> str:
    sections = []
    if file_info:
        sections.append(format_file_info_html(file_info))
    if df is not None:
        sections.append(format_df_info_html(df))
    return "\n".join(sections)
