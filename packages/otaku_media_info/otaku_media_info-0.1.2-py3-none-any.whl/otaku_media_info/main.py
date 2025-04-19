# coding: utf-8

from pathlib import Path

from . import bangumi


def parse(
    file_path: Path,
) -> bangumi.BangumiMediaInfo:
    if not file_path.exists():
        raise ValueError("File does not exist")

    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError("File is empty")

    ext = file_path.suffix.lower()

    if ext in [".mp4", ".mkv"]:
        return bangumi.parse(file_path)

    raise NotImplementedError(f"Unsupported file type: {ext}")


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m otaku_media_info <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    result = parse(file_path)

    print(result)
