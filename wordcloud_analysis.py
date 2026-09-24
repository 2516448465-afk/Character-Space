"""中文文本词频统计与词云生成工具。

用法:
    python wordcloud_analysis.py [输入文件] [--top N] [--output-dir DIR]

默认输入文件为 手推车.txt，生成:
    - output/wordcloud.png      词云图
    - output/word_frequencies.csv 全部词频统计（按频率降序）
"""

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

import jieba
import matplotlib
from wordcloud import WordCloud

matplotlib.use("Agg")  # 无界面环境

# 常用中文停用词（高频无意义词）
STOPWORDS = {
    "的", "了", "是", "在", "我", "他", "她", "它", "和", "与", "及", "或",
    "一个", "我们", "他们", "你们", "自己", "这", "那", "这个", "那个",
    "有", "没", "没有", "不", "不是", "也", "都", "还", "又", "就", "才",
    "要", "会", "能", "可以", "应该", "因为", "所以", "但是", "而", "而且",
    "并且", "如果", "虽然", "然而", "于是", "然后", "之", "以", "为", "对",
    "从", "到", "向", "被", "把", "给", "让", "上", "下", "中", "里", "外",
    "个", "了", "着", "过", "地", "得", "吗", "呢", "吧", "啊", "呀",
    "人们", "的人", "一些", "什么", "怎么", "如何", "其中", "这些", "那些",
    "来说", "起来", "出来", "时候", "时", "后", "前", "等", "以及", "通过",
    "进行", "开始", "已经", "非常", "十分", "更加", "最", "很", "太", "更",
    "其", "此", "之", "者", "或", "即", "并", "则", "于", "由", "将", "作为",
}


def preprocess(text: str) -> str:
    """文本预处理：去除空白、标点、英文和数字，只保留中文。"""
    return "".join(re.findall(r"[\u4e00-\u9fff]+", text))


def segment(text: str, stopwords: set[str]) -> list[str]:
    """jieba 分词 + 停用词过滤 + 去掉单字词。"""
    words = jieba.lcut(preprocess(text))
    return [
        w for w in words
        if len(w) >= 2 and w not in stopwords and re.fullmatch(r"[\u4e00-\u9fff]+", w)
    ]


def find_chinese_font() -> str | None:
    """在系统中查找可用的中文字体文件。"""
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # 兜底（无中文）
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="中文词频统计与词云生成")
    parser.add_argument("input_file", nargs="?", default="手推车.txt")
    parser.add_argument("--top", type=int, default=150, help="进入词云的高频词数量（100~200）")
    parser.add_argument("-o", "--output-dir", default="output")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8")
    words = segment(text, STOPWORDS)
    freq = Counter(words)

    if not freq:
        raise SystemExit("分词结果为空，请检查输入文件。")

    # 保存全部词频（按频率降序）
    csv_path = out_dir / "word_frequencies.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["排名", "词", "频次"])
        for rank, (word, count) in enumerate(freq.most_common(), 1):
            writer.writerow([rank, word, count])

    # 前 20 词
    top20 = freq.most_common(20)
    print(f"总字符数（中文）: {len(preprocess(text))}")
    print(f"分词总数（过滤后）: {len(words)}，不同词数: {len(freq)}")
    print("\n词频前 20：")
    for i, (w, c) in enumerate(top20, 1):
        print(f"{i:>3}. {w:<10} {c}")

    # 生成词云：字号与词频成正比（WordCloud 默认即按频率比例缩放）
    top_words = dict(freq.most_common(args.top))
    font_path = find_chinese_font()
    wc = WordCloud(
        font_path=font_path,
        width=1200,
        height=800,
        background_color="white",
        max_words=args.top,
        colormap="viridis",
        prefer_horizontal=0.95,
    )
    wc.generate_from_frequencies(top_words)
    png_path = out_dir / "wordcloud.png"
    wc.to_file(str(png_path))

    print(f"\n词云已保存: {png_path}（使用前 {args.top} 个高频词）")
    print(f"词频统计已保存: {csv_path}")


if __name__ == "__main__":
    main()
