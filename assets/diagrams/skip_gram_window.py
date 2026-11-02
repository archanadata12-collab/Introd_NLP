"""Draw assets/skip_gram_window.png: the window around the target word "whales" and the pairs it gives.

The sentence is the field guide's "Blue whales usually occur singly or in pairs." after stop-word removal.

Run from the repository root: uv run python assets/diagrams/skip_gram_window.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent.parent / "skip_gram_window.png"
INK, GRAY, BLUE, AMBER, PALE = "#222222", "#6b6b6b", "#2f6fb0", "#c47612", "#fdf6ec"
TOKENS = ["blue", "whales", "usually", "occur", "singly", "pairs"]
TARGET, WINDOW = 1, 5

fig, ax = plt.subplots(figsize=(12.4, 4.4), dpi=200)
fig.patch.set_facecolor("white")
ax.set_xlim(0, 12.4)
ax.set_ylim(0.1, 4.4)
ax.axis("off")

width, gap, y = 1.7, 0.28, 3.0
xs = [0.55 + i * (width + gap) for i in range(len(TOKENS))]
lo, hi = max(0, TARGET - WINDOW), min(len(TOKENS) - 1, TARGET + WINDOW)
ax.add_patch(FancyBboxPatch((xs[lo] - 0.12, y - 0.22), xs[hi] + width - xs[lo] + 0.24, 1.0,
                            boxstyle="round,pad=0.02,rounding_size=0.12", facecolor=PALE, edgecolor=AMBER,
                            linewidth=1.4, linestyle="--"))
ax.text((xs[lo] + xs[hi] + width) / 2, y + 0.95, "window: up to 5 words on each side (here the whole sentence)", ha="center", va="bottom",
        fontsize=11, color=AMBER)
for i, (x, token) in enumerate(zip(xs, TOKENS)):
    color = BLUE if i == TARGET else (INK if lo <= i <= hi else GRAY)
    ax.add_patch(FancyBboxPatch((x, y), width, 0.56, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=BLUE if i == TARGET else "white", edgecolor=color, linewidth=1.5))
    ax.text(x + width / 2, y + 0.28, token, ha="center", va="center", fontsize=12.5,
            color="white" if i == TARGET else color)

contexts = [i for i in range(lo, hi + 1) if i != TARGET]
for k, i in enumerate(contexts):
    px = 0.25 + k * 2.42
    ax.text(px, 1.25, f"(whales, {TOKENS[i]})", fontsize=11.5, color=INK, va="center", family="monospace")
    ax.add_patch(FancyArrowPatch((xs[i] + width / 2, y - 0.05), (px + 0.8, 1.5), arrowstyle="-|>,head_length=5,head_width=3",
                                 color=GRAY, linewidth=1, connectionstyle="arc3,rad=0.0"))
ax.text(0.3, 0.45, "Five training pairs (target, context). The window then moves on, and the next word becomes the target.",
        fontsize=11, color=GRAY, va="center")
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("wrote", OUT)
