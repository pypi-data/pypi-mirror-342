# utils.py
import codecs
import os
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Dict
import chardet
import csv


def is_file_exists(path: str) -> bool:
    return Path(path).exists()


def get_file_name_and_extension(path: str) -> Dict[str, str]:
    p = Path(path)
    return {
        "file_name": p.stem,
        "file_extension": p.suffix
    }


def get_file_size(path: str) -> int:
    return os.path.getsize(path)


def get_file_timestamps(path: str) -> Dict[str, datetime]:
    stat = Path(path).stat()
    return {
        "created_at": datetime.fromtimestamp(stat.st_ctime),
        "modified_at": datetime.fromtimestamp(stat.st_mtime)
    }


def get_file_mime_type(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


def is_compressed_file(path: str) -> bool:
    return path.endswith((".zip", ".gz", ".tar", ".bz2"))

def detect_utf8_sig(file_path: str) -> bool:
    with open(file_path, "rb") as f:
        raw = f.read()
    return raw.startswith(codecs.BOM_UTF8)


def detect_korean_encoding(file_path: str) -> str:
    """
    한국에서 자주 사용되는 인코딩을 감지 (UTF-8, CP949, EUC-KR, UTF-16)
    Returns:
        str: 감지된 인코딩 or 'unsupported' or 'unknown'
    """
    SUPPORTED_EXT = (
        ".txt", ".csv", ".tsv", ".json", ".xml", ".html", ".htm",
        ".py", ".js", ".java", ".php", ".log"
    )

    if not file_path.lower().endswith(SUPPORTED_EXT):
        return "unsupported"

    if not os.path.isfile(file_path):
        return "unknown"

    if detect_utf8_sig(file_path):
        return "UTF-8-SIG"

    for enc in ["utf-8", "cp949", "euc-kr", "utf-16"]:
        try:
            with open(file_path, "rb") as f:
                f.read().decode(enc)
            return enc.upper()
        except UnicodeDecodeError:
            continue

    return "unknown"

# def detect_utf8_sig(file_path):
#     with open(file_path, "rb") as f:
#         raw = f.read()
#
#     if raw.startswith(codecs.BOM_UTF8):
#         return "UTF-8-SIG"
#
#     try:
#         raw.decode("utf-8")
#         return "UTF-8"
#     except UnicodeDecodeError:
#         return None
#
# def detect_korean_encoding(file_path):
#     """ 한국에서 주로 쓰이는 인코딩 확인 """
#     SUPPORTED_FILE_TYPES = (
#         ".txt", ".csv", "tsv", ".json", ".xml", ".html", ".htm",
#         ".py", ".js", ".java", ".php", ".log"
#     )
#
#     # 지원하지 않는 파일 확장자 확인
#     if not file_path.lower().endswith(SUPPORTED_FILE_TYPES):
#         return "unsupported"
#
#     # 파일 존재 여부 확인
#     if not os.path.isfile(file_path):
#         return "unknown"
#
#
#     encodings = {
#         "utf-8-sig": detect_utf8_sig(file_path),
#         "cp949": "cp949",
#         "euc-kr": "EUC-KR",
#         "utf-16": "UTF-16",
#     }
#
#     # UTF-8-SIG 여부 확인
#     if encodings["utf-8-sig"]:
#         return encodings["utf-8-sig"]
#
#     # 나머지 인코딩 체크
#     for encoding, name in encodings.items():
#         if encoding != "utf-8-sig":
#             try:
#                 with open(file_path, "rb") as f:
#                     f.read().decode(encoding)
#                 return name
#             except UnicodeDecodeError:
#                 pass
#
#     return "이 파일은 위의 5가지 인코딩이 아닐 가능성이 높습니다."


def detect_chardet_file_encoding(file_path: str) -> str:
    """
    파일의 인코딩을 추출.
    :param file_path: 파일 경로
    :return: 인코딩 타입 문자열. 감지 실패 시 "unknown" 반환.
    """
    SUPPORTED_FILE_TYPES = (
        ".txt", ".csv", "tsv", ".json", ".xml", ".html", ".htm",
        ".py", ".js", ".java", ".php", ".log"
    )

    # 지원하지 않는 파일 확장자 확인
    if not file_path.lower().endswith(SUPPORTED_FILE_TYPES):
        return "unsupported"

    # 파일 존재 여부 확인
    if not os.path.isfile(file_path):
        return "unknown"

    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(1024 * 10)  # 파일의 일부를 읽어서 인코딩을 감지
            result = chardet.detect(raw_data)
            encoding = result.get("encoding")

            # EUC-KR을 cp949로 매핑
            if encoding == "EUC-KR":
                return "cp949"

            return encoding or "unknown"
    except Exception as e:
        # 예외 발생 시 안전한 기본값 반환
        print(f"Error detecting file encoding: {e}")
        return "unknown"

def detect_file_encoding(path: str) -> str:
    """
        파일 인코딩 감지 로직
        """
    encoding = detect_korean_encoding(path)
    return encoding if encoding != "unsupported" else detect_chardet_file_encoding(path)


def detect_delimiter(
    path: str,
    encoding: str,
    possible_delimiters: list[str] = None
) -> str:
    """
    파일에서 구분자를 추정하는 함수.

    Args:
        path (str): 파일 경로.
        encoding (str): 파일 인코딩.
        possible_delimiters (list): 예상되는 구분자 리스트.

    Returns:
        str: 가장 적합한 구분자.
    """
    if possible_delimiters is None:
        possible_delimiters = [',', '\t', ';', '|', ' ']

    encoding = None if encoding == "unsupported" else encoding

    try:
        with open(path, 'r', encoding=encoding) as file:
            first_line = file.readline().strip()

        def column_count(delim: str) -> int:
            return len(first_line.split(delim))

        best_delimiter = max(possible_delimiters, key=column_count)
        return best_delimiter
    except Exception as e:
        return None