# setup.py

from setuptools import setup, find_packages

setup(
    name="file-inspector",
    version="0.1.4",
    description="파일 메타정보 추출 및 리포트 포맷 변환 유틸",
    author="Song Seung Hwan",
    author_email="shdth117@gmail.com",
    url="https://github.com/alkaline2018/file-inspector",
    packages=find_packages(include=["file_inspector", "file_inspector.*"]),
    include_package_data=True,
    install_requires=[
        "chardet==5.2.0",
        "et_xmlfile==2.0.0",
        "numpy==2.2.4",
        "openpyxl==3.1.5",
        "pandas==2.2.3",
        "python-dateutil==2.9.0.post0",
        "pytz==2025.2",
        "setuptools==78.1.0",
        "six==1.17.0",
        "tabulate==0.9.0",
        "tzdata==2025.2"
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="file inspection report slack markdown html json csv xlsx",
    license="MIT",
    entry_points={
        "console_scripts": [
            "file-inspector=file_inspector.cli:main",
        ],
    }
)