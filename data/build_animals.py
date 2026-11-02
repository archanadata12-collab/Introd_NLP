"""Write data/animals.csv: paragraphs about whales and about horses, one paragraph per row.

Four Project Gutenberg books, two about each animal. From the two horse books only the parts that
are about the horse are taken: chapter V of Allen, and the report itself without its index. The two
sides are then cut to the same number of words, so neither animal dominates the vocabulary. The
repository already contains the result; this script documents how it was made.

Run from the repository root: uv run python data/build_animals.py
"""

import re
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent
MIN_WORDS = 25  # anything shorter is a heading, a caption, a table row or a line of the contents
TYPOGRAPHIC = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})

# One row per book: the animal, a short name for the source, the file, and the two heading lines
# between which the text about that animal stands. What lies outside them is a preface, a table of
# contents, a bibliography, an index or a list of addresses, none of which is prose about an animal.
BOOKS = [
    ("whales", "Leatherwood", "whales_dolphins_porpoises.txt", "ABSTRACT", "ACKNOWLEDGMENTS"),
    ("whales", "Walker", "whale_primer.txt", "Introduction", "Appendix"),
    ("horses", "Allen", "domestic_animals.txt", "CHAPTER V.", "CHAPTER VI."),
    ("horses", "USDA", "diseases_of_the_horse.txt", "THE EXAMINATION OF A SICK HORSE.", "INDEX."),
]


def read_book(path):
    """Return the text of a Project Gutenberg book without its header and licence."""
    text = path.read_text(encoding="utf-8")
    start = text.find("\n", text.find("*** START OF"))  # the end of the START line
    end = text.find("*** END OF")
    return text[start:end].strip()


def cut(text, start, end):
    """Return the lines of the text between the heading line `start` and the heading line `end`.

    The headings are indented differently from book to book, so the lines are compared stripped.
    """
    lines = text.split("\n")
    stripped = [line.strip() for line in lines]
    return "\n".join(lines[stripped.index(start) + 1:stripped.index(end)])


def normalize(text):
    """Return the text with straight quotes, no italic underscores and no double hyphens.

    The underscores matter more than they look: a tokenizer's `\\b` counts `_` as a word character,
    so `_Physeter_` and `_causes_` would match no word at all and the italics would vanish.
    """
    text = text.translate(TYPOGRAPHIC)
    text = re.sub(r"_(\w[^_]*)_", r"\1", text)
    return text.replace("--", " ")


def paragraphs(text):
    """Return the paragraphs of a text as single lines, without the short ones.

    A figure in a Project Gutenberg text is written [Illustration: its caption]. The caption is
    prose about the animal and stays; the marker around it is not and goes.
    """
    text = normalize(text.replace("[Illustration: ", "").replace("[Illustration]", ""))
    kept = []
    for block in re.split(r"\n\s*\n", text):
        paragraph = " ".join(block.split())
        if len(paragraph.split()) >= MIN_WORDS:
            kept.append(paragraph)
    return kept


def balanced(rows):
    """Return the rows of both subjects, each cut to the word count of the shorter side."""
    table = pd.DataFrame(rows)
    table["words"] = table["text"].str.split().str.len()
    budget = table.groupby("subject")["words"].sum().min()
    kept = table[table.groupby("subject")["words"].cumsum() <= budget]
    return kept.drop(columns="words").reset_index(drop=True)


if __name__ == "__main__":
    rows = []
    for subject, source, name, start, end in BOOKS:
        text = cut(read_book(DATA / name), start, end)
        rows += [{"subject": subject, "source": source, "text": paragraph} for paragraph in paragraphs(text)]
    animals = balanced(rows)
    animals.to_csv(DATA / "animals.csv", index=False)
    print(animals.groupby(["subject", "source"])["text"].agg(
        paragraphs="size", words=lambda texts: texts.str.split().str.len().sum()).to_string())
