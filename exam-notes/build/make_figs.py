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


def clean_axes(ax):
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)


# --------------------------------------------------------------------------- SVM
@fig("svm_margin")
def _():
    f, ax = plt.subplots(figsize=(4.6, 3.6))
    pos = [(5.6, 6.4), (6.5, 5.4), (7.2, 6.8), (6.2, 7.6), (7.6, 5.0), (5.0, 7.3)]
    neg = [(1.6, 2.2), (2.6, 1.4), (1.2, 3.4), (2.2, 3.0), (3.2, 2.0), (1.0, 1.4)]
    sv_pos = [(4.6, 5.4), (5.6, 4.4)]
    sv_neg = [(3.4, 2.6), (2.4, 3.6)]
    ax.scatter(*zip(*pos), marker="o", s=34, facecolor="black")
    ax.scatter(*zip(*neg), marker="s", s=34, facecolor="white", edgecolor="black")
    ax.scatter(*zip(*sv_pos), marker="o", s=34, facecolor="black")
    ax.scatter(*zip(*sv_neg), marker="s", s=34, facecolor="white", edgecolor="black")
    for p in sv_pos + sv_neg:
        ax.add_patch(Circle(p, 0.32, fill=False, lw=1.0))
    xs = np.linspace(0, 9, 10)
    ax.plot(xs, 8 - xs, "k-", lw=1.4)
    ax.plot(xs, 10.0 - xs, "k--", lw=0.9)
    ax.plot(xs, 6.0 - xs, "k--", lw=0.9)
    ax.annotate("", xy=(4.5, 5.5), xytext=(2.5, 3.5), arrowprops=dict(arrowstyle="<->", lw=0.9))
    ax.text(2.2, 5.6, "margin\n" + r"$=\dfrac{2}{\Vert w\Vert}$", fontsize=10, ha="center")
    ax.text(6.9, 1.35, r"$w\cdot x+b=0$", fontsize=10)
    ax.text(7.6, 2.75, r"$w\cdot x+b=+1$", fontsize=9)
    ax.text(5.15, 0.25, r"$w\cdot x+b=-1$", fontsize=9)
    ax.text(7.0, 7.9, "Class +1", fontsize=9); ax.text(0.4, 0.4, "Class -1", fontsize=9)
    ax.text(4.9, 4.0, "support\nvectors", fontsize=8.5, ha="left", style="italic")
    ax.set_xlim(0, 9); ax.set_ylim(0, 8.6); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); clean_axes(ax)
    save(f, "svm_margin")


@fig("svm_kernel")
def _():
    f, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8))
    neg = np.array([-3, -2.5, -2, 2, 2.6, 3])
    pos = np.array([-1, -0.5, 0, 0.5, 1])
    a.scatter(neg, 0 * neg, marker="s", s=36, facecolor="white", edgecolor="black")
    a.scatter(pos, 0 * pos, marker="o", s=36, facecolor="black")
    a.axhline(0, color="black", lw=0.8); a.set_yticks([]); a.set_ylim(-1, 1)
    a.set_title("Input space (1-D): not separable", fontsize=10); a.set_xlabel("$x$"); clean_axes(a)
    a.spines["left"].set_visible(False)
    b.scatter(neg, neg ** 2, marker="s", s=36, facecolor="white", edgecolor="black")
    b.scatter(pos, pos ** 2, marker="o", s=36, facecolor="black")
    b.axhline(2.5, color="black", ls="--", lw=1.1); b.text(-3.2, 2.8, "linear separator", fontsize=9)
    b.set_title(r"Feature space $\phi(x)=(x,\,x^2)$: separable", fontsize=10)
    b.set_xlabel("$x$"); b.set_ylabel("$x^2$"); clean_axes(b)
    f.tight_layout()
    save(f, "svm_kernel")


# --------------------------------------------------------------------------- Data Analytics
@fig("da_clique_grid")
def _():
    f, ax = plt.subplots(figsize=(4.4, 3.6))
    rng = np.random.default_rng(3)
    c1 = rng.normal([2.5, 6.5], 0.35, (40, 2)); c2 = rng.normal([6.5, 2.5], 0.4, (40, 2))
    noise = rng.uniform(0, 9, (25, 2))
    pts = np.vstack([c1, c2, noise])
    for (cx, cy) in [(2, 6), (6, 2), (2, 7), (6, 3), (7, 2)]:
        cnt = ((pts[:, 0] >= cx) & (pts[:, 0] < cx + 1) & (pts[:, 1] >= cy) & (pts[:, 1] < cy + 1)).sum()
        if cnt >= 5:
            ax.add_patch(Rectangle((cx, cy), 1, 1, fc="0.82", ec="none"))
    ax.scatter(pts[:, 0], pts[:, 1], s=6, color="black")
    for v in range(10):
        ax.axvline(v, color="black", lw=0.4); ax.axhline(v, color="black", lw=0.4)
    ax.set_xlim(0, 9); ax.set_ylim(0, 9); ax.set_xlabel("Dimension 1 (e.g. age)"); ax.set_ylabel("Dimension 2 (e.g. salary)")
    ax.set_xticks([]); ax.set_yticks([])
    save(f, "da_clique_grid")


@fig("da_pca")
def _():
    f, ax = plt.subplots(figsize=(4.0, 3.6))
    X = np.array([(2, 1), (3, 5), (4, 3), (5, 6), (6, 7), (7, 8)], float)
    ax.scatter(X[:, 0], X[:, 1], s=34, color="black")
    for p in X:
        ax.annotate("(%d,%d)" % tuple(p), p, textcoords="offset points", xytext=(5, -10), fontsize=8.5)
    m = X.mean(0); v1 = np.array([0.5696, 0.8219]); v2 = np.array([-0.8219, 0.5696])
    for v, t, L in [(v1, "PC1", 4.8), (v2, "PC2", 1.6)]:
        ax.annotate("", xy=m + L * v, xytext=m - L * v, arrowprops=dict(arrowstyle="-|>", lw=1.1))
        ax.text(*(m + L * v + 0.15), t, fontsize=10)
    ax.plot(*m, marker="+", ms=10, color="black"); ax.text(m[0] + 0.15, m[1] - 0.55, "mean (4.5, 5)", fontsize=8.5)
    ax.set_xlim(0, 10); ax.set_ylim(-0.5, 10); ax.set_aspect("equal"); ax.set_xlabel("x"); ax.set_ylabel("y"); clean_axes(ax)
    save(f, "da_pca")


@fig("da_kmeans8")
def _():
    f, ax = plt.subplots(figsize=(4.0, 3.8))
    P = {"A1": (2, 10), "A2": (2, 5), "A3": (8, 4), "A4": (5, 8), "A5": (7, 5), "A6": (6, 4), "A7": (1, 2), "A8": (4, 9)}
    groups = [(["A1", "A4", "A8"], "o", "black", (3.67, 9)), (["A3", "A5", "A6"], "s", "white", (7, 4.33)), (["A2", "A7"], "^", "white", (1.5, 3.5))]
    for names, mk, fc, c in groups:
        pts = [P[n] for n in names]
        ax.scatter(*zip(*pts), marker=mk, s=44, facecolor=fc, edgecolor="black")
        ax.scatter([c[0]], [c[1]], marker="x", s=70, color="black", linewidths=1.6)
        for n in names:
            ax.annotate(n, P[n], textcoords="offset points", xytext=(5, 4), fontsize=9)
    ax.add_patch(Ellipse((3.7, 9.0), 4.4, 2.8, fill=False, ls="--", lw=0.8))
    ax.add_patch(Ellipse((7.0, 4.4), 3.0, 2.2, fill=False, ls="--", lw=0.8))
    ax.add_patch(Ellipse((1.5, 3.5), 2.0, 4.4, fill=False, ls="--", lw=0.8))
    ax.text(5.2, 10.4, "Cluster 1", fontsize=9); ax.text(7.6, 5.7, "Cluster 2", fontsize=9); ax.text(0.0, 6.0, "Cluster 3", fontsize=9)
    ax.set_xlim(-0.5, 10); ax.set_ylim(0, 11.5); ax.set_xlabel("x"); ax.set_ylabel("y"); clean_axes(ax)
    save(f, "da_kmeans8")


@fig("da_hadoop_ecosystem")
def _():
    f, ax = blank(7.4, 4.0)
    def box(x, y, w, h, t, fs=10, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec="black", lw=1.0))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal")
    box(0, 0, 9, 0.7, "HDFS  -  Hadoop Distributed File System (storage)", 11, True)
    box(0, 0.85, 7.2, 0.7, "YARN  -  resource management & job scheduling", 11, True)
    box(7.35, 0.85, 1.65, 2.35, "HBase\n(NoSQL\ncolumn\nstore)")
    box(0, 1.7, 2.3, 0.65, "MapReduce\n(batch)"); box(2.45, 1.7, 2.3, 0.65, "Spark\n(in-memory)"); box(4.9, 1.7, 2.3, 0.65, "Tez")
    box(0, 2.5, 1.7, 0.7, "Pig\n(Pig Latin)"); box(1.82, 2.5, 1.7, 0.7, "Hive\n(HiveQL)"); box(3.64, 2.5, 1.7, 0.7, "Mahout /\nMLlib"); box(5.46, 2.5, 1.74, 0.7, "Spark SQL /\nStreaming")
    box(0, 3.35, 4.4, 0.6, "Data ingestion:\nSqoop (RDBMS), Flume, Kafka (streams)", 9)
    box(4.55, 3.35, 4.45, 0.6, "Coordination & management:\nZooKeeper, Oozie, Ambari", 9)
    ax.set_xlim(-0.1, 9.1); ax.set_ylim(-0.1, 4.05)
    save(f, "da_hadoop_ecosystem")


@fig("da_lifecycle")
def _():
    f, ax = blank(6.4, 5.2)
    labels = ["1. Discovery", "2. Data\nPreparation", "3. Model\nPlanning", "4. Model\nBuilding", "5. Communicate\nResults", "6. Operationalize"]
    qs = ["Enough info to\ndraft a plan?", "Is the data\ngood enough?", "Good idea for\nthe model?", "Is the model\nrobust?", "", ""]
    R = 2.0
    ang = [90 - 60 * i for i in range(6)]
    P = [(R * np.cos(np.radians(a)), R * np.sin(np.radians(a))) for a in ang]
    for (x, y), t in zip(P, labels):
        ax.add_patch(FancyBboxPatch((x - 0.72, y - 0.33), 1.44, 0.66, boxstyle="round,pad=0.02,rounding_size=0.12", fc="white", ec="black", lw=1.2))
        ax.text(x, y, t, ha="center", va="center", fontsize=10.5, weight="bold")
    for i in range(6):
        a, b = P[i], P[(i + 1) % 6]
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=1.2, color="black",
                                     connectionstyle="arc3,rad=-0.22", shrinkA=30, shrinkB=30))
    for i in range(1, 4):
        a, b = P[i], P[i - 1]
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=10, lw=0.8, color="black", ls="--",
                                     connectionstyle="arc3,rad=-0.25", shrinkA=24, shrinkB=24))
    ax.text(0, 0, "Data\nAnalytics\nLifecycle", ha="center", va="center", fontsize=11)
    ax.set_xlim(-3, 3); ax.set_ylim(-2.6, 2.6)
    save(f, "da_lifecycle")


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(REGISTRY)
    for n in names:
        REGISTRY[n]()
        print("figure:", n)
