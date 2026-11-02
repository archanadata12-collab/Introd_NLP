"""Draw assets/embedding_network.png: the network of notebook 02, a one-hot input over the 500-word vocabulary, a
hidden layer of 2 neurons without activation (the embedding) and a softmax output over the same 500 words; the
hidden weights form the embedding matrix.

Run from the repository root: uv run python assets/diagrams/embedding_network.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = Path(__file__).parent.parent / "embedding_network.png"
INK, GRAY, BLUE, AMBER, GREEN, PALE = "#222222", "#6b6b6b", "#2f6fb0", "#c47612", "#3a8a4f", "#fdf6ec"
INPUTS = ["whale", "horse", "...", "fin", "...", "feed"]
OUTPUTS = ["dolphins", "minke", "...", "dorsal", "...", "species"]

fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
fig.patch.set_facecolor("white")
ax.set_xlim(0, 12)
ax.set_ylim(-1.7, 6.4)
ax.set_aspect("equal")
ax.axis("off")


def column(x, labels, values, color, title, value_side):
    """Draw one layer as a column of neurons; return their centers."""
    ys = [5.0 - i * 0.9 for i in range(len(labels))]
    centers = []
    for y, label, value in zip(ys, labels, values):
        if label == "...":
            ax.text(x, y, "⋮", ha="center", va="center", fontsize=16, color=GRAY)
            centers.append(None)
            continue
        ax.add_patch(Circle((x, y), 0.28, facecolor="white", edgecolor=color, linewidth=1.5))
        ax.text(x, y, value, ha="center", va="center", fontsize=10.5, color=INK)
        if value_side == "left":
            ax.text(x - 0.45, y, label, ha="right", va="center", fontsize=10.5, color=GRAY)
        else:
            ax.text(x + 0.45, y, label, ha="left", va="center", fontsize=10.5, color=GRAY)
        centers.append((x, y))
    ax.text(x, 5.85, title, ha="center", va="bottom", fontsize=11.5, color=color, linespacing=1.3)
    return centers


inputs = column(2.2, INPUTS, ["1", "0", "", "0", "", "0"], INK, "one-hot input\n500 words", "left")
hidden = [(6.0, 3.65), (6.0, 2.35)]
for i, (x, y) in enumerate(hidden):
    ax.add_patch(Circle((x, y), 0.32, facecolor=PALE, edgecolor=AMBER, linewidth=1.8))
    ax.text(x, y, f"e{i + 1}", ha="center", va="center", fontsize=11, color=INK)
ax.text(6.0, 5.85, "hidden layer\n2 neurons, no activation", ha="center", va="bottom", fontsize=11.5, color=AMBER,
        linespacing=1.3)
outputs = column(9.8, OUTPUTS, ["p", "p", "", "p", "", "p"], GREEN, "softmax output\n500 words", "right")

for start in inputs:
    if start:
        for end in hidden:
            color, width = (BLUE, 1.6) if start[1] == 5.0 else (GRAY, 0.5)
            ax.plot([start[0] + 0.28, end[0] - 0.32], [start[1], end[1]], color=color, linewidth=width, zorder=0)
for start in hidden:
    for end in outputs:
        if end:
            ax.plot([start[0] + 0.32, end[0] - 0.28], [start[1], end[1]], color=GRAY, linewidth=0.5, zorder=0)

ax.add_patch(FancyBboxPatch((0.9, -1.55), 10.2, 1.15, boxstyle="round,pad=0.02,rounding_size=0.1", facecolor=PALE,
                            edgecolor=AMBER, linewidth=1))
ax.text(6.0, -0.975, "The weights from the input to the hidden layer form a 500 × 2 matrix.\n"
        "The one-hot vector of \"whale\" selects one row of it (blue): the embedding of \"whale\".",
        ha="center", va="center", fontsize=9.5, color=INK, linespacing=1.5)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("wrote", OUT)
