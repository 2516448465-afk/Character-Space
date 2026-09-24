import argparse
import re
from pathlib import Path

import jieba


def segment_text(text: str) -> list[str]:
    """对中文文本分词，并保留中文词语。"""
    words = jieba.lcut(text)
    return [word for word in words if re.fullmatch(r"[\u4e00-\u9fff]+", word)]


def main() -> None:
    parser = argparse.ArgumentParser(description="中文文本分词工具")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="明史.txt",
        help="待处理的文本文件，默认是明史.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="分词结果.txt",
        help="分词结果保存路径，默认是分词结果.txt",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output)
    words = segment_text(input_path.read_text(encoding="utf-8"))
    output_path.write_text(" ".join(words), encoding="utf-8")

    print(f"共分出 {len(words)} 个词")
    print(" / ".join(words[:100]))
    print(f"结果已保存到：{output_path}")


if __name__ == "__main__":
    main() 