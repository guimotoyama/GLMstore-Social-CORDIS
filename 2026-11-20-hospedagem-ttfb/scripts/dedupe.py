from PIL import Image
import glob, os, sys

TILES = sys.argv[1]
OUT   = sys.argv[2]
DUR   = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
FPS   = int(sys.argv[4])   if len(sys.argv) > 4 else 25
THRESH = float(sys.argv[5]) if len(sys.argv) > 5 else 0.45

files = sorted(glob.glob(os.path.join(TILES, 'f*.png')))
print('tiles lidos:', len(files))
os.makedirs(OUT, exist_ok=True)

kept = []
last = None
for f in files:
    im = Image.open(f).convert('L').resize((96, 168))
    px = list(im.getdata())
    if last is not None:
        d = sum(abs(a-b) for a, b in zip(px, last)) / len(px)
        if d <= THRESH:
            continue
    kept.append(f)
    last = px

print('distintos apos dedupe:', len(kept))

N = int(DUR * FPS)
if len(kept) < N:
    print('AVISO: distintos < %d; repetindo a ultima' % N)
    while len(kept) < N:
        kept.append(kept[-1])

idx = [round(i * (len(kept)-1) / (N-1)) for i in range(N)]
seen = set()
for n, k in enumerate(idx):
    if k in seen and k+1 < len(kept):
        k += 1
    seen.add(k)
    Image.open(kept[k]).save(os.path.join(OUT, 'f%04d.png' % n))
print('frames gravados:', N, '| duracao %.1fs @ %d fps' % (DUR, FPS))
