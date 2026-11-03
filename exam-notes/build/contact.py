"""Make contact sheets (grids of page thumbnails) from a PDF for quick visual review."""
import sys, glob, os, subprocess
from PIL import Image
pdf, out, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
tmp = out + "_pages"; os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.png"): os.remove(f)
subprocess.run(["pdftoppm", "-r", "45", "-png", "-f", str(first), "-l", str(last), pdf, tmp + "/p"], check=True)
ims = [Image.open(f) for f in sorted(glob.glob(tmp + "/*.png"))]
cols = 4; w, h = ims[0].size
for k in range(0, len(ims), 8):
    chunk = ims[k:k + 8]; rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "white")
    for i, im in enumerate(chunk):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(f"{out}_{k // 8 + 1}.png")
    print(f"{out}_{k // 8 + 1}.png")
