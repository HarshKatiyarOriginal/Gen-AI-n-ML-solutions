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


@fig("dbms_checkpoint")
def _():
    f, ax = plt.subplots(figsize=(6.6, 2.7))
    tc, tf = 4.0, 8.0
    rows = [("T1", 0.4, 3.0, True, "ignore (committed before Tc)"),
            ("T2", 1.5, 5.5, True, "REDO"),
            ("T3", 2.5, None, False, "UNDO"),
            ("T4", 4.6, 6.8, True, "REDO"),
            ("T5", 6.0, None, False, "UNDO")]
    for i, (n, s0, e, done, act) in enumerate(rows):
        y = 5 - i
        end = e if done else tf
        ax.plot([s0, end], [y, y], color="black", lw=2.2 if done else 1.4, ls="-" if done else "--")
        ax.plot([s0], [y], marker="|", ms=10, color="black")
        if done:
            ax.plot([end], [y], marker="|", ms=10, color="black")
        ax.text(-0.25, y, n, ha="right", va="center", fontsize=10)
        ax.text(8.25, y, act, ha="left", va="center", fontsize=9.5, weight="bold" if act != "ignore (committed before Tc)" else "normal")
    for x, t in [(tc, "$T_c$ (checkpoint)"), (tf, "$T_f$ (crash)")]:
        ax.axvline(x, color="black", lw=0.9)
        ax.text(x, 5.75, t, ha="center", fontsize=10)
    ax.set_xlim(-0.8, 11.8); ax.set_ylim(0.4, 6.1); ax.axis("off")
    ax.annotate("time", xy=(8.0, 0.55), xytext=(0, 0.55), arrowprops=dict(arrowstyle="-|>", lw=0.8), va="center", fontsize=9)
    save(f, "dbms_checkpoint")


@fig("web_positioning")
def _():
    f, ax = blank(6.2, 4.2)
    def rect(x, y, w, h, t=None, ls="-", lw=1.1, fc="white", fs=9.5, va="center"):
        ax.add_patch(Rectangle((x, y), w, h, fill=True, fc=fc, ec="black", ls=ls, lw=lw))
        if t: ax.text(x + w / 2, y + h / 2 if va == "center" else y + h - 0.18, t, ha="center", va=va, fontsize=fs)
    rect(0, 0, 10, 6.6, None, lw=1.6)
    ax.text(0.15, 6.35, "VIEWPORT (browser window)", fontsize=9, va="center")
    rect(6.6, 5.6, 3.2, 0.8, "FIXED: stays here\nwhen page scrolls", lw=1.6)
    rect(0.4, 0.3, 9.2, 5.0, None, ls="--")
    ax.text(0.55, 5.05, "Parent  (position: relative)", fontsize=9, va="center")
    rect(0.8, 4.0, 3.0, 0.65, "static box 1 (normal flow)")
    rect(0.8, 3.1, 3.0, 0.65, "static box 2")
    rect(0.8, 2.2, 3.0, 0.65, None, ls=":")
    ax.text(2.3, 2.52, "original place (gap kept)", fontsize=8, ha="center", style="italic")
    rect(1.6, 1.75, 3.0, 0.65, "RELATIVE: shifted", lw=1.6)
    ax.annotate("", xy=(1.6, 2.1), xytext=(0.8, 2.55), arrowprops=dict(arrowstyle="-|>", lw=0.8))
    rect(0.8, 0.6, 3.0, 0.65, "static box 3")
    rect(6.3, 3.7, 3.0, 1.1, "ABSOLUTE\ntop: 10px; right: 10px\n(out of normal flow)", lw=1.6)
    ax.set_xlim(-0.1, 10.1); ax.set_ylim(-0.1, 6.7)
    save(f, "web_positioning")


@fig("daa_asymptotic")
def _():
    f, axs = plt.subplots(1, 3, figsize=(8.4, 2.5))
    n = np.linspace(0.2, 10, 200)
    g = n
    curves = [("Big-O:  f(n) ≤ c·g(n)", [(1.6 * g, r"$c\,g(n)$", "-"), (g + 2.5 * np.sin(n) * np.exp(-n / 4) + 0.8, r"$f(n)$", "--")]),
              ("Big-Ω:  f(n) ≥ c·g(n)", [(0.6 * g, r"$c\,g(n)$", "-"), (g + 1.5 * np.sin(n) * np.exp(-n / 4) + 0.6, r"$f(n)$", "--")]),
              (r"Big-Θ:  $c_1 g(n) \leq f(n) \leq c_2 g(n)$", [(1.5 * g, r"$c_2\,g(n)$", "-"), (0.55 * g, r"$c_1\,g(n)$", "-"), (g + 1.2 * np.sin(n) * np.exp(-n / 3) + 0.5, r"$f(n)$", "--")])]
    for ax, (title, cs) in zip(axs, curves):
        for y, lab, ls in cs:
            ax.plot(n, y, "k", ls=ls, lw=1.2)
            ax.text(10.15, y[-1], lab, fontsize=9, va="center")
        ax.axvline(3, color="black", lw=0.6, ls=":"); ax.text(3, -1.2, "$n_0$", ha="center", fontsize=10)
        ax.set_title(title, fontsize=9.5); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 12); ax.set_ylim(0, 16)
        ax.set_xlabel("n", fontsize=9); clean_axes(ax)
    f.tight_layout()
    save(f, "daa_asymptotic")


@fig("daa_pnp")
def _():
    f, ax = blank(6.4, 4.0)
    ax.add_patch(Ellipse((3.0, 2.0), 5.4, 3.6, fill=False, lw=1.4))
    ax.add_patch(Ellipse((2.2, 1.55), 2.4, 1.6, fill=False, lw=1.2))
    ax.add_patch(Ellipse((5.0, 3.35), 4.6, 2.3, fill=False, lw=1.4, ls="--"))
    ax.text(0.95, 2.95, "NP", fontsize=15, weight="bold")
    ax.text(2.2, 1.75, "P", fontsize=15, weight="bold", ha="center")
    ax.text(2.2, 1.2, "Sorting, MST,\nDijkstra, Search", fontsize=8.5, ha="center")
    ax.text(4.35, 3.05, "NP-Complete", fontsize=11, weight="bold", ha="center")
    ax.text(4.35, 2.55, "SAT, 3-SAT, Clique,\nVertex Cover, Ham. Cycle", fontsize=8.5, ha="center")
    ax.text(6.0, 4.05, "NP-Hard", fontsize=13, weight="bold", ha="center")
    ax.text(6.2, 3.55, "Halting problem,\nTSP (optimization)", fontsize=8.5, ha="center")
    ax.text(3.0, -0.25, r"NP-Complete = NP $\cap$ NP-Hard;   P $\subseteq$ NP", fontsize=10, ha="center", style="italic")
    ax.set_xlim(0, 7.5); ax.set_ylim(-0.5, 4.6)
    save(f, "daa_pnp")


@fig("daa_4queens")
def _():
    f, axs = plt.subplots(1, 2, figsize=(5.6, 2.9))
    for ax, sol, t in [(axs[0], (2, 4, 1, 3), "Solution 1: (2, 4, 1, 3)"), (axs[1], (3, 1, 4, 2), "Solution 2: (3, 1, 4, 2)")]:
        for r in range(4):
            for c in range(4):
                ax.add_patch(Rectangle((c, 3 - r), 1, 1, fc="0.85" if (r + c) % 2 else "white", ec="black", lw=0.8))
        for r, c in enumerate(sol):
            ax.text(c - 0.5, 3 - r + 0.5, "♛", ha="center", va="center", fontsize=22, family="DejaVu Sans")
        for i in range(4):
            ax.text(i + 0.5, 4.15, str(i + 1), ha="center", fontsize=9); ax.text(-0.2, 3.5 - i, str(i + 1), ha="right", va="center", fontsize=9)
        ax.set_xlim(-0.5, 4.1); ax.set_ylim(-0.1, 4.6); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t, fontsize=10, y=-0.12)
    save(f, "daa_4queens")


@fig("ml_regression")
def _():
    f, ax = plt.subplots(figsize=(4.2, 3.0))
    x = np.array([1, 2, 3, 4, 5]); y = np.array([2, 4, 5, 4, 5]); yh = 2.2 + 0.6 * x
    xs = np.linspace(0.5, 5.5, 10); ax.plot(xs, 2.2 + 0.6 * xs, "k-", lw=1.4)
    for xi, yi, hi in zip(x, y, yh):
        ax.plot([xi, xi], [yi, hi], "k:", lw=1)
    ax.scatter(x, y, s=36, color="black", zorder=3)
    ax.text(4.0, 3.05, r"$\hat{y} = 2.2 + 0.6x$", fontsize=11)
    ax.text(1.12, 2.4, r"residual $e_i$", fontsize=9, style="italic")
    ax.set_xlim(0.5, 5.6); ax.set_ylim(1.5, 5.6); ax.set_xlabel("x"); ax.set_ylabel("y"); clean_axes(ax)
    save(f, "ml_regression")


@fig("ml_gradient")
def _():
    f, ax = plt.subplots(figsize=(4.4, 3.0))
    t = np.linspace(-4.6, 4.6, 200); ax.plot(t, t ** 2, "k-", lw=1.3)
    th = [4.0]
    for _ in range(5):
        th.append(th[-1] - 0.1 * 2 * th[-1] * 1.6)
    for a, b in zip(th[:-1], th[1:]):
        ax.annotate("", xy=(b, b ** 2), xytext=(a, a ** 2), arrowprops=dict(arrowstyle="-|>", lw=1.0))
    ax.scatter(th, [v ** 2 for v in th], s=22, color="black", zorder=3)
    ax.text(4.05, 16.4, r"start $\theta_0$", fontsize=9)
    ax.text(0, -1.6, "minimum (gradient = 0)", fontsize=9, ha="center")
    ax.text(-4.4, 17, r"$\theta_{new} = \theta_{old} - \alpha\,\frac{dJ}{d\theta}$", fontsize=11)
    ax.set_xlabel(r"$\theta$"); ax.set_ylabel(r"$J(\theta)$"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-2.5, 22); clean_axes(ax)
    save(f, "ml_gradient")


@fig("ml_overfit")
def _():
    f, ax = plt.subplots(figsize=(5.0, 3.0))
    n = np.linspace(0, 10, 200)
    train = 0.55 + 0.43 * (1 - np.exp(-n / 2.5)); test = 0.55 + 0.3 * (1 - np.exp(-n / 2)) - 0.022 * np.maximum(n - 3.5, 0) ** 1.3
    ax.plot(n, train, "k-", lw=1.4, label="Training accuracy"); ax.plot(n, test, "k--", lw=1.4, label="Test accuracy")
    ax.axvline(3.6, color="black", lw=0.7, ls=":")
    ax.text(1.4, 0.5, "UNDERFITTING\n(high bias)", ha="center", fontsize=8.5); ax.text(3.6, 0.5, "best\nsize", ha="center", fontsize=8.5)
    ax.text(7.5, 0.5, "OVERFITTING\n(high variance)", ha="center", fontsize=8.5)
    ax.annotate("pruning", xy=(4.0, 0.80), xytext=(7.0, 0.88), arrowprops=dict(arrowstyle="-|>", lw=0.8), fontsize=9)
    ax.set_xlabel("Tree size (number of nodes)"); ax.set_ylabel("Accuracy"); ax.set_xticks([]); ax.set_ylim(0.42, 1.02)
    ax.legend(frameon=False, fontsize=9, loc="lower right"); clean_axes(ax)
    save(f, "ml_overfit")


@fig("ml_knn")
def _():
    f, ax = plt.subplots(figsize=(3.8, 3.2))
    A = [(1, 1), (2, 1), (1, 2)]; B = [(4, 3), (5, 4)]
    ax.scatter(*zip(*A), marker="o", s=50, facecolor="black", label="Class A")
    ax.scatter(*zip(*B), marker="s", s=50, facecolor="white", edgecolor="black", label="Class B")
    ax.scatter([3], [2], marker="*", s=150, color="black"); ax.text(3.12, 2.08, "query ?", fontsize=9)
    ax.add_patch(Circle((3, 2), 2.02, fill=False, ls="--", lw=0.9)); ax.text(3.5, 0.15, "k = 3 neighbours", fontsize=8.5)
    for p, n in [((1, 1), "P1"), ((2, 1), "P2"), ((4, 3), "P3"), ((5, 4), "P4"), ((1, 2), "P5")]:
        ax.annotate(n, p, textcoords="offset points", xytext=(5, 4), fontsize=8.5)
    ax.set_xlim(-0.2, 6); ax.set_ylim(-0.2, 4.8); ax.set_aspect("equal"); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); clean_axes(ax)
    save(f, "ml_knn")


@fig("ml_and_xor")
def _():
    f, axs = plt.subplots(1, 2, figsize=(5.6, 2.6))
    for ax, title, out in [(axs[0], "AND (linearly separable)", {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}),
                           (axs[1], "XOR (NOT linearly separable)", {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0})]:
        for (a, b), v in out.items():
            ax.scatter([a], [b], s=70, marker="o", facecolor="black" if v else "white", edgecolor="black", zorder=3)
            ax.text(a + 0.07, b + 0.07, str(v), fontsize=10)
        ax.set_title(title, fontsize=10); ax.set_xlim(-0.4, 1.5); ax.set_ylim(-0.4, 1.5); ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); clean_axes(ax)
    xs = np.linspace(-0.4, 1.5, 10); axs[0].plot(xs, 1.5 - xs, "k--", lw=1.1)
    axs[1].text(0.55, 0.45, "no single\nline works", ha="center", fontsize=8.5, style="italic")
    f.tight_layout()
    save(f, "ml_and_xor")


@fig("ml_gridworld")
def _():
    f, ax = blank(4.4, 3.4)
    grid = [["→", "→", "→", "GOAL\n+1"], ["↑", "WALL", "↑", "PIT\n−1"], ["START\n↑", "→", "↑", "←"]]
    for r in range(3):
        for c in range(4):
            t = grid[r][c]
            fc = "0.75" if t == "WALL" else "white"
            ax.add_patch(Rectangle((c, 2 - r), 1, 1, fc=fc, ec="black", lw=1.1))
            fs = 18 if len(t) == 1 else 9.5
            ax.text(c + 0.5, 2 - r + 0.5, t, ha="center", va="center", fontsize=fs, family="DejaVu Sans" if len(t) == 1 else None, weight="bold" if len(t) > 1 else "normal")
    ax.set_xlim(-0.05, 4.05); ax.set_ylim(-0.05, 3.05)
    save(f, "ml_gridworld")


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(REGISTRY)
    for n in names:
        REGISTRY[n]()
        print("figure:", n)
