"""Segment the novel into tokenized sentences for later reuse.

Reads data/novel.txt, converts it to simplified Chinese (jieba works
better with simplified characters), splits it into sentences on Chinese
sentence-ending punctuation, tokenizes each sentence with jieba while
removing punctuation, keeps sentences with at least 5 words, and writes
the result to sentences.txt (one sentence per line, words separated by
single spaces).
"""

import re

import jieba
import opencc

INPUT_PATH = "data/novel.txt"
OUTPUT_PATH = "sentences.txt"

# Proper nouns that jieba would otherwise split into multiple tokens.
USER_DICT = ["沃兰德"]

# Sentence-ending punctuation used to split the text.
SENTENCE_ENDINGS = "。！？"

# All punctuation marks to strip during tokenization
# (Chinese + ASCII).
PUNCTUATION = set(
    "，。！？；：、·…—“”‘’（）〔〕【】《》〈〉「」『』［］｛｝"
    "～％＋－＝＄＾｜＼／＿＠＃＄"
    ",.!?;:\"'()[]{}<>~%^|\\/@#$&_-=+*"
)


def is_punctuation(text: str) -> bool:
    return all(ch in PUNCTUATION or ch.isspace() for ch in text)


def main() -> None:
    with open(INPUT_PATH, encoding="utf-8") as f:
        text = f.read()

    for word in USER_DICT:
        jieba.add_word(word)

    converter = opencc.OpenCC("t2s")
    text = converter.convert(text)

    # Split into sentences, keeping the ending punctuation attached.
    sentences = re.findall(rf"[^{SENTENCE_ENDINGS}]+[{SENTENCE_ENDINGS}]?", text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for sentence in sentences:
            words = [
                word for word in jieba.cut(sentence)
                if not is_punctuation(word)
            ]
            if len(words) >= 5:
                f.write(" ".join(words) + "\n")

    print(f"done: wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
