"""Write data/poems.csv: the poems of the two Project Gutenberg books, one poem or poem section per row.

Each book is cut into documents with regular expressions, then normalized with the normalize function below. The repository already contains the result; this script documents how it was made.

Run from the repository root: uv run python data/build_poems.py
"""

import re
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent
TYPOGRAPHIC = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})


def read_book(path):
    """Return the text of a Project Gutenberg book without its header and licence."""
    text = path.read_text(encoding="utf-8")
    start = text.find("\n", text.find("*** START OF"))  # the end of the START line
    end = text.find("*** END OF")
    return text[start:end].strip()


def split_dickinson(text):
    """Return a list of dictionaries with the author, title and text of every poem of Dickinson's book.

    Poems start after a line with only a Roman numeral, such as IV.; a poem may start with a title in capitals.
    """
    text = text[text.find("I. LIFE."):]  # skip the editors' preface
    text = re.sub(r"\n{3,}POEMS\n.*?(?=\nI\. LIFE\.)", "\n", text, flags=re.DOTALL)  # series 2 and 3 prefaces
    text = re.sub(r"^[IVX]+\. [A-Z ]+\.$", "", text, flags=re.MULTILINE)  # section headings such as II. LOVE.
    text = re.sub(r"\[[^\]]*\]", "", text)  # editorial notes in brackets
    text = re.sub(r"^NOTE\..*?(?=\n\n|\Z)", "", text, flags=re.MULTILINE | re.DOTALL)  # notes after NOTE.

    poems, pending_title = [], None
    for block in re.split(r"^[IVXLC]+\.$", text, flags=re.MULTILINE):
        lines = block.strip().split("\n")
        title = None
        if lines[0].isupper() and lines[0].endswith("."):  # a title such as SUCCESS.
            title, lines = lines[0].rstrip("."), lines[1:]
        poem = "\n".join(lines).strip()
        if not poem:  # a title on its own line, followed by numbered parts of one poem
            pending_title = title
            continue
        poems.append({"author": "Dickinson", "title": title or pending_title, "text": poem})
        pending_title = None
    return poems


def split_whitman(text):
    """Return a list of dictionaries with the author, title and text of every poem or numbered section.

    Poems are separated by at least three line breaks and start with an unindented title line; long poems are
    divided into sections headed by a line with only a number.
    """
    text = text[text.find("BOOK I."):]
    text = re.sub(r"^BOOK ?[IVXL]+\..*$", "", text, flags=re.MULTILINE)  # book headings
    poems = []
    for poem in re.split(r"\n{3,}(?=\S)", text):
        title, _, verses = poem.strip().partition("\n")
        for section in re.split(r"^ +\d+$", verses, flags=re.MULTILINE):  # numbered sections
            if section.strip():
                poems.append({"author": "Whitman", "title": title.strip(), "text": section.strip("\n")})
    return poems


def normalize(text):
    """Return the text with straight quotes, no italic underscores and no double hyphens ."""
    text = text.translate(TYPOGRAPHIC)
    text = re.sub(r"_(\w[^_]*)_", r"\1", text)
    return text.replace("--", " ")


if __name__ == "__main__":
    poems = pd.DataFrame(
        split_dickinson(read_book(DATA / "dickinson_poems.txt")) + split_whitman(read_book(DATA / "whitman_leaves_of_grass.txt"))
    )
    poems["text"] = poems["text"].map(normalize)
    poems.to_csv(DATA / "poems.csv", index=False)
    print(poems["author"].value_counts().to_string())
