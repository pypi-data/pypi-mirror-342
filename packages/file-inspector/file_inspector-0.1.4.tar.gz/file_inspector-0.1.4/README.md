# 📦 file-inspector

**file-inspector**는 다양한 형식의 파일을 자동 분석하고, Slack 메시지, Markdown, HTML, JSON 포맷 등으로 리포트를 생성해주는 Python 기반 경량 라이브러리입니다. 
데이터 수집 · 검증 · 리포트 자동화가 필요한 프로젝트에서 매우 유용하게 활용될 수 있습니다.

---

## ✅ 주요 기능

| 기능 | 설명 |
|------|------|
| 파일 정보 추출 | 경로, 이름, 확장자, 크기, 인코딩, 구분자, MIME, 생성/수정일 등 |
| 파일 읽기 | `.csv`, `.xlsx`, `.json`, `.parquet` 지원 |
| 출력 포맷 | Slack, Markdown, HTML, JSON 형태로 리포트 생성 |
| 유효성 검사 | 특정 컬럼 존재 여부 확인, 누락 컬럼 목록 추출 |
| 통계 요약 | `describe()` 기반 기술 통계 제공 |
| 샘플 미리보기 | 상위 n개 행 출력 (`head()`) |
| 일괄 분석 | 폴더 내 모든 파일을 순회하며 분석 수행 |

---

## 📁 프로젝트 구조

```bash
file-inspector/
├── file_inspector/         # 핵심 패키지
│   ├── inspector.py        # 메인 클래스 (FileInspector, FileInspectionResult)
│   ├── file_reader.py      # 파일 읽기 전담
│   ├── file_info_extractor.py  # 메타 정보 추출
│   ├── schema_validator.py     # 컬럼 유효성 검사
│   ├── utils.py            # 공통 유틸 함수
│   ├── types.py            # 타입 정의
│   └── formatter/          # 다양한 출력 포맷
│       ├── slack_formatter.py
│       ├── markdown_formatter.py
│       ├── html_formatter.py
│       └── json_formatter.py
├── examples/               # 사용 예제
├── tests/                  # 테스트 코드
├── data/                   # 예제용 샘플 파일
├── README.md
├── .gitignore
├── pyproject.toml
├── setup.py
└── requirements.txt
```

---

## 📦 설치 방법

```bash
# 기본 설치
pip install -e .
```

---

## 🚀 사용 예제

```python
from file_inspector import FileInspector
inspector = FileInspector()
result = inspector.inspect("data/sample.csv")

print(result.to_dict())                 # 기본 정보 dict
print(result.to_markdown())            # Markdown 출력 (Notion용)
print(result.to_html())                # HTML 출력
print(result.to_json())                # JSON 출력
print(result.validate_schema(["id"])) # 필수 컬럼 체크
```

---

## 🧪 테스트

```bash
python -m unittest discover tests
```

---

## 🔍 사용 기술 및 설계 원칙

- **Python 3.9+**
- **Pandas 기반 DataFrame 처리**
- **SOLID 원칙 기반 설계**
- **클린 코드와 책임 분리 구조**
- **단일 책임 클래스 분리 (Reader, Extractor, Validator, Formatter 등)**

---

## 📜 라이선스

MIT License

---

## 👏 기여

PR과 이슈는 언제나 환영입니다. 더 많은 포맷터, 클라우드 업로더, Notion 연동 기능 등도 확장 가능합니다.
