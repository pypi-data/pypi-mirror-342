# file_inspector/__init__.py

"""
file_inspector 패키지는 다양한 파일을 읽고, 정보를 추출하고,
다양한 포맷으로 리포트를 제공하는 기능을 제공합니다.

이 패키지는 다음의 주요 클래스를 포함합니다:
- FileInspector: 파일 분석의 메인 진입점
- FileInspectionResult: 분석 결과를 담고 다양한 출력 포맷 지원

서브모듈:
- file_reader: pandas 기반의 파일 읽기 기능
- file_info_extractor: 파일 메타데이터 추출
- schema_validator: DataFrame 컬럼 유효성 검사
- formatter: 출력 포맷 (Slack, Markdown, HTML 등)
"""

from .inspector import FileInspector, FileInspectionResult