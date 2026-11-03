#!/usr/bin/env bash
# Build the AKTU revision notebook (Markdown + PDF) from exam-notes/src/*.md
# Requires: pandoc, graphviz (dot), python3 + matplotlib, node + playwright (Chromium),
#           TeX Gyre fonts (fonts-texgyre).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
OUT="${1:-$ROOT/AKTU_Revision_Notebook.pdf}"

ORDER="${ORDER:-u1 u2 u3 u4 u5 w1 w2 w3 w4 w5 d1 d2 d3 d4 d5 m1 m2 m3 m4 m5 m6 a1 a2 a3 a4 a5 a6 c1 c2 c3 c4 c5}"
FILES=()
for f in $ORDER; do [ -f "$ROOT/src/$f.md" ] && FILES+=("$ROOT/src/$f.md"); done

# 1. regenerate matplotlib figures
python3 "$HERE/make_figs.py" >/dev/null

# 2. join sources; make sure every list is preceded by a blank line (pandoc needs it)
python3 - "$ROOT/AKTU_Revision_Notebook.md" "${FILES[@]}" <<'PY'
import re, sys
out, files = sys.argv[1], sys.argv[2:]
li = re.compile(r'^\s*(- |\d+\. )')
res = []
for f in files:
    code = False
    prev = ""
    for line in open(f, encoding="utf-8").read().split("\n"):
        if line.lstrip().startswith("```"):
            code = not code
        elif (not code and li.match(line) and prev.strip() and not li.match(prev)
              and not prev.startswith("  ")):
            res.append("")
        res.append(line)
        prev = line
    res.append("")
open(out, "w", encoding="utf-8").write("\n".join(res))
PY

# 3. Markdown -> HTML (Graphviz figures, MathML maths) -> PDF
cd "$ROOT"
pandoc "$ROOT/AKTU_Revision_Notebook.md" -s --mathml \
  --lua-filter "$HERE/figures.lua" --highlight-style=monochrome \
  --metadata pagetitle="AKTU Revision Notebook" \
  -c "$HERE/style.css" --embed-resources \
  -o "$ROOT/build/notebook.html"

node "$HERE/topdf.js" "$ROOT/build/notebook.html" "$OUT"
echo "Built $OUT"
