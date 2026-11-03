"""Matplotlib figures for the AKTU revision notebook (plots, networks, grids).

Run:  python3 build/make_figs.py      -> writes SVG files into exam-notes/figures/
Each figure is a small function registered with @fig("name").
Style: black-and-white textbook look, serif font, no colour.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Ellipse, FancyBboxPatch
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["TeX Gyre Termes", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.edgecolor": "black",
    "axes.linewidth": 0.9,
    "lines.color": "black",
    "svg.fonttype": "path",
})

REGISTRY = {}


def fig(name):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


def save(f, name):
    f.savefig(os.path.join(OUT, name + ".svg"), bbox_inches="tight", transparent=True)
    plt.close(f)


def arrow(ax, p, q, text=None, frac=0.3, offset=(0, 0.12), lw=1.0, style="-|>", ls="-", fs=10, shrink=14):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, lw=lw, color="black",
                        linestyle=ls, shrinkA=shrink, shrinkB=shrink)
    ax.add_patch(a)
    if text:
        x = p[0] + (q[0] - p[0]) * frac + offset[0]
        y = p[1] + (q[1] - p[1]) * frac + offset[1]
        ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def neuron(ax, xy, label, r=0.28, fs=12):
    ax.add_patch(Circle(xy, r, fc="white", ec="black", lw=1.2, zorder=3))
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=fs, zorder=4)


def blank(w, h):
    f, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return f, ax


# --------------------------------------------------------------------------- ML
@fig("ml_backprop_net")
def _():
    f, ax = blank(7.2, 3.6)
    I = {"i1": (0, 2.2), "i2": (0, 0.6)}
    H = {"h1": (3, 2.2), "h2": (3, 0.6)}
    O = {"o1": (6, 2.2), "o2": (6, 0.6)}
    for k, p in I.items():
        neuron(ax, p, "$%s_%s$" % (k[0], k[1]))
    for k, p in H.items():
        neuron(ax, p, "$%s_%s$" % (k[0], k[1]))
    for k, p in O.items():
        neuron(ax, p, "$%s_%s$" % (k[0], k[1]))
    arrow(ax, I["i1"], H["h1"], "$w_1=0.15$", 0.45, (0, 0.18))
    arrow(ax, I["i2"], H["h1"], "$w_2=0.20$", 0.25, (0, 0.05))
    arrow(ax, I["i1"], H["h2"], "$w_3=0.25$", 0.25, (0, -0.05))
    arrow(ax, I["i2"], H["h2"], "$w_4=0.30$", 0.45, (0, -0.18))
    arrow(ax, H["h1"], O["o1"], "$w_5=0.40$", 0.45, (0, 0.18))
    arrow(ax, H["h2"], O["o1"], "$w_6=0.45$", 0.25, (0, 0.05))
    arrow(ax, H["h1"], O["o2"], "$w_7=0.50$", 0.25, (0, -0.05))
    arrow(ax, H["h2"], O["o2"], "$w_8=0.55$", 0.45, (0, -0.18))
    for p, t in [((1.5, -0.55), "$b_1=0.35$"), ((4.5, -0.55), "$b_2=0.60$")]:
        ax.add_patch(FancyBboxPatch((p[0] - 0.42, p[1] - 0.2), 0.84, 0.4, boxstyle="round,pad=0.02",
                                    fc="white", ec="black"))
        ax.text(*p, t, ha="center", va="center", fontsize=10)
    for tgt in [H["h1"], H["h2"]]:
        arrow(ax, (1.5, -0.35), tgt, ls="--", lw=0.8, shrink=8)
    for tgt in [O["o1"], O["o2"]]:
        arrow(ax, (4.5, -0.35), tgt, ls="--", lw=0.8, shrink=8)
    ax.text(-0.75, 2.2, "0.05", ha="right", va="center")
    ax.text(-0.75, 0.6, "0.10", ha="right", va="center")
    ax.text(6.45, 2.2, r"$\rightarrow\ t_1=0.01$", ha="left", va="center")
    ax.text(6.45, 0.6, r"$\rightarrow\ t_2=0.99$", ha="left", va="center")
    for x, t in [(0, "Input layer"), (3, "Hidden layer"), (6, "Output layer")]:
        ax.text(x, 3.0, t, ha="center", fontsize=10, style="italic")
    ax.set_xlim(-1.4, 7.9); ax.set_ylim(-0.9, 3.2)
    save(f, "ml_backprop_net")


@fig("ml_kmeans_clusters")
def _():
    f, ax = plt.subplots(figsize=(4.6, 3.3))
    c1 = [(185, 72), (179, 68), (182, 72), (188, 77)]
    c2 = [(170, 56), (168, 60)]
    names = {(185, 72): "P1", (170, 56): "P2", (168, 60): "P3", (179, 68): "P4", (182, 72): "P5", (188, 77): "P6"}
    ax.scatter(*zip(*c1), marker="o", s=40, facecolor="black", edgecolor="black", label="Cluster 1")
    ax.scatter(*zip(*c2), marker="s", s=40, facecolor="white", edgecolor="black", label="Cluster 2")
    ax.scatter([183.5, 169], [72.25, 58], marker="x", s=80, color="black", linewidths=1.6, label="Centroid")
    for p, n in names.items():
        ax.annotate(n, p, textcoords="offset points", xytext=(5, 4), fontsize=9)
    ax.add_patch(Ellipse((183.5, 72.5), 13, 13, fill=False, ls="--", lw=0.8))
    ax.add_patch(Ellipse((169, 58), 6, 8, fill=False, ls="--", lw=0.8))
    ax.set_xlabel("Height"); ax.set_ylabel("Weight")
    ax.set_xlim(163, 193); ax.set_ylim(50, 82)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    save(f, "ml_kmeans_clusters")


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(REGISTRY)
    for n in names:
        REGISTRY[n]()
        print("figure:", n)
