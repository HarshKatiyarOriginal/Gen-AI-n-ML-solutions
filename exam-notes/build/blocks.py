"""List or replace UNTAGGED ``` code blocks (old ASCII diagrams / formulas) in a source file.
   python3 build/blocks.py list  src/w1.md
   python3 build/blocks.py show  src/w1.md 0,2
   python3 build/blocks.py apply src/w1.md patch.py   (patch.py defines R = {index: "new markdown"})
Tagged blocks (```html, ```dot, ...) are never touched."""
import sys

def parse(lines):
    """Return list of (start, end) line indexes (inclusive) of untagged fenced blocks."""
    res, i, n = [], 0, len(lines)
    while i < n:
        st = lines[i].strip()
        if st.startswith("```"):
            tag = st[3:].strip()
            j = i + 1
            while j < n and lines[j].strip() != "```":
                j += 1
            if tag == "":
                res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res

cmd, path = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().split("\n")
B = parse(lines)
if cmd == "list":
    for k, (a, b) in enumerate(B):
        body = [l.strip() for l in lines[a + 1:b] if l.strip()][:2]
        print(k, "|", " // ".join(x[:70] for x in body))
elif cmd == "show":
    for k in map(int, sys.argv[3].split(",")):
        a, b = B[k]; print(f"--- {k} ---"); print("\n".join(lines[a + 1:b]))
else:
    ns = {}; exec(open(sys.argv[3], encoding="utf-8").read(), ns); R = ns["R"]
    out, last = [], 0
    for k, (a, b) in enumerate(B):
        out += lines[last:a]
        out += (R[k].strip("\n").split("\n") if k in R else lines[a:b + 1])
        last = b + 1
    out += lines[last:]
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print("replaced", len(R), "of", len(B))
