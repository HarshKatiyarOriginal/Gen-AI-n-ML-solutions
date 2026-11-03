#!/usr/bin/env bash
# Build the short, exam-style notes: exam_src/<name>.md -> pdf/exam/<name>.pdf
# {{fig:FILE:N}} inside exam_src is replaced by figure N of src/FILE.md (see build/figlist.py).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/.." && pwd)"
mkdir -p "$ROOT/pdf/exam" "$ROOT/build/tmp"
python3 "$HERE/make_figs.py" >/dev/null
NAMES="${*:-$(cd "$ROOT/exam_src" && ls *.md | sed 's/\.md$//')}"
for n in $NAMES; do
  python3 - "$ROOT" "$n" <<'PY'
import re, sys
sys.path.insert(0, sys.argv[1] + "/build")
from figlist import figures
root, n = sys.argv[1], sys.argv[2]
text = open(f"{root}/exam_src/{n}.md", encoding="utf-8").read()
cache = {}
def fig(m):
    f, k = m.group(1), int(m.group(2))
    if f not in cache: cache[f] = figures(open(f"{root}/src/{f}.md", encoding="utf-8").read())
    return cache[f][k]
text = re.sub(r"\{\{fig:(\w+):(\d+)\}\}", fig, text)
li = re.compile(r'^\s*(- |\d+\. )'); out = []; code = False; prev = ""
for line in text.split("\n"):
    if line.lstrip().startswith("```"): code = not code
    elif not code and li.match(line) and prev.strip() and not li.match(prev) and not prev.startswith("  "): out.append("")
    out.append(line); prev = line
open(f"{root}/build/tmp/{n}.md", "w", encoding="utf-8").write("\n".join(out))
PY
  (cd "$ROOT" && pandoc "build/tmp/$n.md" -s --mathml --lua-filter "$HERE/figures.lua" --highlight-style=monochrome \
     --metadata pagetitle="$n" -c "$HERE/exam.css" --embed-resources -o "build/tmp/$n.html")
  node "$HERE/topdf.js" "$ROOT/build/tmp/$n.html" "$ROOT/pdf/exam/$n.pdf"
  echo "Built pdf/exam/$n.pdf ($(pdfinfo "$ROOT/pdf/exam/$n.pdf" | awk '/Pages/{print $2}') pages)"
done
