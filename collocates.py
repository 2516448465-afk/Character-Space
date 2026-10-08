"""Find collocates for the target word "沃兰德" in the segmented novel.

Reads sentences.txt (one space-separated sentence per line) and runs
qhchina's find_collocates three times (window h=5, window h=10, sentence),
keeping only non-stopword collocates of at least 2 characters with a
p-value below 0.05. Each result is sorted by obs_local (descending),
saved to its own CSV in output/, and its top 20 rows printed.
"""

import os

import qhchina
from qhchina.analytics.collocations import find_collocates

INPUT_PATH = "sentences.txt"
OUTPUT_DIR = "output"
TARGET_WORD = "沃兰德"
MIN_WORD_LENGTH = 2
P_THRESHOLD = 0.05

RUNS = [
    {"name": "window_h5", "method": "window", "horizon": 5},
    {"name": "window_h10", "method": "window", "horizon": 10},
    {"name": "sentence", "method": "sentence", "horizon": None},
]


def load_sentences(path: str) -> list[list[str]]:
    with open(path, encoding="utf-8") as f:
        return [line.split() for line in f if line.strip()]


def main() -> None:
    sentences = load_sentences(INPUT_PATH)
    stopwords = qhchina.load_stopwords()
    filters = {
        "stopwords": stopwords,
        "min_word_length": MIN_WORD_LENGTH,
        "max_p": P_THRESHOLD,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for run in RUNS:
        result = find_collocates(
            sentences,
            TARGET_WORD,
            method=run["method"],
            horizon=run["horizon"],
            filters=filters,
        )
        if len(result) > 0:
            result = result.sort_values("obs_local", ascending=False).reset_index(drop=True)
        out_path = os.path.join(OUTPUT_DIR, f"collocates_woland_{run['name']}.csv")
        result.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n=== {run['name']}: {len(result)} collocates -> {out_path} ===")
        print(result.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
