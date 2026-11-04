#!/usr/bin/env bash
# Build the final single AKTU notebook: cover + contents (with page numbers) + all exam_src subjects.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/.." && pwd)"
OUT="$ROOT/pdf/AKTU_Final_Notebook.pdf"
bash "$HERE/build_exam.sh" >/dev/null            # refresh build/tmp/<subject>.md (figures expanded)
SUBJ=$(cd "$ROOT/exam_src" && ls *.md | sed 's/\.md$//')

make_book () {   # $1 = contents HTML block
python3 - "$ROOT" "$1" $SUBJ <<'PY'
import sys
root, toc, subs = sys.argv[1], sys.argv[2], sys.argv[3:]
cover = '''<div class="cover">
<div class="c-top">Dr. A.P.J. Abdul Kalam Technical University (AKTU)</div>
<div class="c-title">AKTU REVISION NOTEBOOK</div>
<div class="c-sub">B.Tech CSE · 3rd Year · Odd Semester</div>
<div class="c-list">Database Management System<br>Web Technology<br>Design and Analysis of Algorithms<br>Machine Learning Techniques<br>Data Analytics<br>Constitution of India, Law &amp; Engineering</div>
<div class="c-sub">Exam answers in topper answer-sheet style<br>Section A (2 marks) · Section B (7 marks) · Solved numericals</div>
<div class="c-name">Harsh Katiyar · PSIT</div>
</div>'''
parts = [cover, toc]
for s in subs:
    parts.append(open(f"{root}/build/tmp/{s}.md", encoding="utf-8").read())
open(f"{root}/build/tmp/FINAL.md", "w", encoding="utf-8").write("\n\n".join(parts))
PY
(cd "$ROOT" && pandoc build/tmp/FINAL.md -s --mathml --lua-filter "$HERE/figures.lua" --highlight-style=monochrome \
   --metadata pagetitle="AKTU Revision Notebook" -c "$HERE/exam.css" -c "$HERE/final.css" --embed-resources -o build/tmp/FINAL.html)
node "$HERE/topdf.js" "$ROOT/build/tmp/FINAL.html" "$OUT"
}

PLACEHOLDER='<div class="toc"><div class="toc-h">CONTENTS</div><p>placeholder</p></div>'
make_book "$PLACEHOLDER"
# pass 2: find the page of every subject and unit heading, then rebuild with real page numbers
TOC=$(python3 - "$OUT" <<'PY'
import subprocess, sys, re
pdf = sys.argv[1]
n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
subjects = ["Database Management System", "Web Technology", "Design and Analysis of Algorithms",
            "Machine Learning Techniques", "Data Analytics", "Constitution of India, Law & Engineering"]
import glob
names = {}
for f in sorted(glob.glob(pdf.rsplit("/pdf/", 1)[0] + "/exam_src/*.md")):
    for l in open(f, encoding="utf-8"):
        if l.startswith("## "): names[l[3:].strip().upper()] = l[3:].strip()
rows, si = [], 0
for p in range(3, n + 1):
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"], capture_output=True, text=True).stdout
    for line in t.split("\n"):
        s = line.strip()
        if si < len(subjects) and s == subjects[si]:
            rows.append(("s", subjects[si], p)); si += 1
        m = re.match(r"^UNIT (\d): (.+)$", s)
        if m and rows:
            rows.append(("u", names.get(s, s), p))
html = ['<div class="toc"><div class="toc-h">CONTENTS</div>']
for kind, name, p in rows:
    cls = "toc-s" if kind == "s" else "toc-u"
    html.append(f'<div class="{cls}"><span>{name}</span><span class="dots"></span><span>{p}</span></div>')
html.append("</div>")
print("".join(html))
PY
)
make_book "$TOC"
echo "Built $OUT ($(pdfinfo "$OUT" | awk '/Pages/{print $2}') pages)"
