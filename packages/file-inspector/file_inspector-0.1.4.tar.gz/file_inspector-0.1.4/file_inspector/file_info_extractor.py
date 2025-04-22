# file_info_extractor.py

from datetime import datetime
from typing import Dict
from . import utils
from .types import IFileInfoExtractor, FileMetaInfo


class FileInfoExtractor(IFileInfoExtractor):
    """
    파일 메타 정보를 추출하는 책임을 가지는 클래스
    - 파일 존재 여부, 경로, 이름, 크기, MIME, 인코딩, 구분자, 생성/수정 시간, 압축 여부
    """

    def extract(self, file_path: str) -> FileMetaInfo:
        confirm_at = datetime.now()

        if not utils.is_file_exists(file_path):
            return FileMetaInfo(
                file_exists=False,
                file_path=file_path,
                confirm_at=confirm_at,
                message="File does not exist"
            )

        encoding = utils.detect_file_encoding(file_path)
        delimiter = utils.detect_delimiter(file_path, encoding)

        name_ext = utils.get_file_name_and_extension(file_path)
        timestamps = utils.get_file_timestamps(file_path)

        return FileMetaInfo(
            file_exists=True,
            file_path=file_path,
            confirm_at=confirm_at,
            file_name=name_ext.get("file_name"),
            extension=name_ext.get("file_extension"),
            file_size=utils.get_file_size(file_path),
            created_at=timestamps.get("created_at"),
            modified_at=timestamps.get("modified_at"),
            mime_type=utils.get_file_mime_type(file_path),
            encoding=encoding,
            delimiter=delimiter,
            is_compressed=utils.is_compressed_file(file_path)
        )