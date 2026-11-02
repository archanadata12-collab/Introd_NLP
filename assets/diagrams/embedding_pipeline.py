"""Draw assets/embedding_pipeline.png: the five steps of notebook 02, each with a small example. A sentence of the
field guide, its (target, context) pairs, the network that predicts the context words, its hidden weights as word
vectors, and the vectors in a plot. The vectors are the ones notebook 02 learns (seed 42).

Run from the repository root: uv run python assets/diagrams/embedding_pipeline.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent.parent / "embedding_pipeline.png"
INK, GRAY, BLUE, AMBER, GREEN, PALE = "#222222", "#6b6b6b", "#2f6fb0", "#c47612", "#3a8a4f", "#fdf6ec"
VECTORS = {  # word: (x, y, color); the two hidden weights notebook 02 learns for the word
    "whale": (0.79, -0.31, BLUE), "whales": (0.98, -0.18, BLUE), "dolphins": (1.30, -0.67, BLUE),
    "fin": (0.74, -1.27, BLUE), "dorsal": (0.63, -1.48, BLUE),
    "horse": (-0.88, 0.52, AMBER), "horses": (-0.58, 0.79, AMBER), "feed": (-0.72, 1.10, AMBER),
    "disease": (-1.42, 0.29, AMBER), "blood": (-1.72, -0.35, AMBER),
    "body": (-0.33, -0.94, GREEN), "animal": (-0.36, -0.21, GREEN),
}

X_MAX, Y_MIN, Y_MAX = 16.3, 0.75, 4.8
fig = plt.figure(figsize=(X_MAX, Y_MAX - Y_MIN), dpi=200)
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)
ax.axis("off")

W, GAP, TOP, BOTTOM = 2.75, 0.5, 4.55, 0.95
xs = [0.25 + i * (W + GAP) for i in range(5)]
TITLES = ["1. Text", "2. Training pairs", "3. Network", "4. Word vectors", "5. Similar words"]
CAPTIONS = ["the four books, split into\nwords without stop words", "each target word with\nthe words in its window",
            "learns to predict the\ncontext words of a target", "the hidden weights:\n2 numbers per word",
            "words with similar\nneighbors lie close"]
for x, title, caption in zip(xs, TITLES, CAPTIONS):
    ax.add_patch(FancyBboxPatch((x, BOTTOM), W, TOP - BOTTOM, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=PALE, edgecolor=AMBER, linewidth=1.4))
    ax.text(x + W / 2, TOP - 0.3, title, ha="center", va="center", fontsize=13, color=AMBER, fontweight="bold")
    ax.text(x + W / 2, BOTTOM + 0.45, caption, ha="center", va="center", fontsize=10, color=GRAY, linespacing=1.4)
for x in xs[:-1]:
    ax.add_patch(FancyArrowPatch((x + W + 0.05, 2.75), (x + W + GAP - 0.05, 2.75), arrowstyle="-|>",
                                 mutation_scale=18, color=GRAY, linewidth=1.5))

# 1. Text: a sentence of the field guide and its tokens
x = xs[0]
ax.text(x + W / 2, 3.55, "\"Blue whales usually occur\nsingly or in pairs.\"", ha="center", va="center", fontsize=10.5,
        color=INK, style="italic", linespacing=1.4)
for k, token in enumerate(["blue", "whales", "usually", "occur", "singly", "pairs"]):
    tx, ty = x + 0.5 + (k % 3) * 0.88, 2.65 - (k // 3) * 0.5
    ax.text(tx, ty, token, ha="center", va="center", fontsize=9, color="white" if token == "whales" else INK,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": BLUE if token == "whales" else "white",
                  "edgecolor": BLUE if token == "whales" else GRAY, "linewidth": 1})

# 2. Pairs: a small table
x = xs[1]
ax.text(x + 0.85, 3.75, "target", ha="center", fontsize=10.5, color=GRAY, fontweight="bold")
ax.text(x + 1.95, 3.75, "context", ha="center", fontsize=10.5, color=GRAY, fontweight="bold")
ax.plot([x + 0.35, x + W - 0.35], [3.65, 3.65], color=GRAY, linewidth=0.8)
for k, context in enumerate(["blue", "usually", "occur", "singly"]):
    ty = 3.35 - k * 0.36
    ax.text(x + 0.85, ty, "whales", ha="center", va="center", fontsize=11, color=BLUE)
    ax.text(x + 1.95, ty, context, ha="center", va="center", fontsize=11, color=INK)

# 3. Network: one-hot input, 2 hidden neurons, softmax output
x = xs[2]
values = ["1", "0", "0", "0", "0"]
inputs = [(x + 0.55, 3.7 - k * 0.36) for k in range(5)]
hidden = [(x + 1.4, 3.25), (x + 1.4, 2.65)]
outputs = [(x + 2.25, 3.7 - k * 0.36) for k in range(5)]
for (ix, iy), value in zip(inputs, values):
    for hx, hy in hidden:
        ax.plot([ix, hx], [iy, hy], color=BLUE if value == "1" else GRAY, linewidth=1.6 if value == "1" else 0.4,
                zorder=1)
for hx, hy in hidden:
    for ox, oy in outputs:
        ax.plot([hx, ox], [hy, oy], color=GRAY, linewidth=0.4, zorder=1)
for (ix, iy), value in zip(inputs, values):
    ax.add_patch(Circle((ix, iy), 0.15, facecolor="white", edgecolor=BLUE if value == "1" else INK, zorder=2))
    ax.text(ix, iy, value, ha="center", va="center", fontsize=8.5, color=INK, zorder=3)
for hx, hy in hidden:
    ax.add_patch(Circle((hx, hy), 0.18, facecolor=PALE, edgecolor=AMBER, linewidth=1.6, zorder=2))
for ox, oy in outputs:
    ax.add_patch(Circle((ox, oy), 0.15, facecolor="white", edgecolor=GREEN, zorder=2))
ax.text(x + 0.55, 1.98, "one-hot\nwhales", ha="center", va="top", fontsize=9, color=BLUE, linespacing=1.2)
ax.text(x + 1.4, 1.98, "2\nneurons", ha="center", va="top", fontsize=9, color=AMBER, linespacing=1.2)
ax.text(x + 2.25, 1.98, "context\nwords", ha="center", va="top", fontsize=9, color=GREEN, linespacing=1.2)

# 4. Word vectors: a table of the learnt values
x = xs[3]
for tx, header in [(x + 0.75, "word"), (x + 1.55, "x"), (x + 2.2, "y")]:
    ax.text(tx, 3.75, header, ha="center", fontsize=10.5, color=GRAY, fontweight="bold")
ax.plot([x + 0.3, x + W - 0.3], [3.65, 3.65], color=GRAY, linewidth=0.8)
for k, word in enumerate(["whale", "dolphins", "horse", "body"]):
    vx, vy, color = VECTORS[word]
    ty = 3.35 - k * 0.36
    ax.text(x + 0.75, ty, word, ha="center", va="center", fontsize=11, color=color)
    ax.text(x + 1.55, ty, f"{vx:.2f}", ha="center", va="center", fontsize=11, color=INK)
    ax.text(x + 2.2, ty, f"{vy:.2f}", ha="center", va="center", fontsize=11, color=INK)

# 5. Similar words: a small scatter plot of the same vectors
x = xs[4]
inset = fig.add_axes([(x + 0.3) / X_MAX, (1.8 - Y_MIN) / (Y_MAX - Y_MIN), (W - 0.6) / X_MAX, 2.1 / (Y_MAX - Y_MIN)])
inset.set_facecolor("white")
for word, (vx, vy, color) in VECTORS.items():
    inset.scatter(vx, vy, color=color, s=22, zorder=2)
    left = word in ("whale", "dorsal", "horse", "disease", "blood", "animal")  # label to the left where it would overlap a neighbor
    inset.annotate(word, (vx, vy), xytext=(-4 if left else 4, 3), textcoords="offset points", fontsize=7.5,
                   color=color, ha="right" if left else "left")
inset.set(xlim=(-2.4, 2.35), ylim=(-1.95, 1.55), xticks=[], yticks=[])
for spine in inset.spines.values():
    spine.set_color(GRAY)
    spine.set_linewidth(0.6)

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("wrote", OUT)
