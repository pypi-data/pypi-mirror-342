import os
import argparse
from file_inspector.inspector import FileInspector


def main():
    parser = argparse.ArgumentParser(description="File Inspector CLI")
    parser.add_argument("path", help="분석할 파일 또는 디렉토리 경로")
    args = parser.parse_args()

    inspector = FileInspector()

    if os.path.isdir(args.path):
        results = inspector.batch_inspect(args.path)
        for result in results:
            print(result.to_dict())
    else:
        result = inspector.inspect(args.path)
        print(result.to_dict())


if __name__ == '__main__':
    main()