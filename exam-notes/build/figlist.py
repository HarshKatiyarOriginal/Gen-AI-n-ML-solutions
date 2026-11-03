"""List the figures (```{.dot} blocks, raw <figure> HTML, ![](figures/..) images) in src files, with indexes.
These can be reused in short notes as {{fig:FILE:INDEX}}."""
import re, sys
def figures(text):
    lines = text.split("\n"); out = []; i = 0
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith("```{.dot"):
            j = i + 1
            while lines[j].strip() != "```": j += 1
            out.append("\n".join(lines[i:j + 1])); i = j + 1; continue
        if l.startswith("![") and "figures/" in l:
            out.append(l)
        if l.startswith('<figure class="fig">'):
            j = i
            while "</figure>" not in lines[j]: j += 1
            out.append("\n".join(lines[i:j + 1])); i = j + 1; continue
        i += 1
    return out
if __name__ == "__main__":
    for f in sys.argv[1:]:
        for k, fg in enumerate(figures(open(f, encoding="utf-8").read())):
            m = re.search(r'caption="([^"]*)"', fg) or re.search(r'!\[([^\]]*)\]', fg) or re.search(r'<figcaption>(.*?)</figcaption>', fg)
            print(f"{f.split('/')[-1][:-3]}:{k} | {(m.group(1) if m else fg.split(chr(10))[0])[:90]}")
