"""Compose scene PNGs using authored timings without encoding video."""
from pathlib import Path
import json
import os
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
BUILD = Path(os.environ.get('EXPLAINER_OUT', str(ROOT.parents[1] / 'out' / 'chapter-02'))).resolve()
# Load drawing definitions and timings, stopping before the encoding loop.
source = (ROOT / 'render.py').read_text().split('renderer=hashlib.sha256')[0]
namespace = {'__file__': str(ROOT / 'render.py')}
exec(compile(source, str(ROOT / 'render.py'), 'exec'), namespace)
previews = BUILD / 'previews'
previews.mkdir(exist_ok=True)
timings = json.loads((BUILD / 'timings.json').read_text())
thumbs = []
for scene in timings:
    layers = namespace['make'](scene)
    variants = [('full', scene['duration'] - 0.1)]
    if len(layers) > 1:
        variants.insert(0, ('initial', 0.3))
    for label, moment in variants:
        image = Image.new('RGBA', (1280, 720), namespace['BG'])
        for layer, start, end in layers:
            if moment >= start and (end is None or moment < end):
                image.alpha_composite(layer)
        image.convert('RGB').save(previews / f"scene-{scene['number']:02}-{label}.png")
        if label == 'full':
            thumb = image.convert('RGB').resize((640, 360))
            thumbs.append(thumb)
contact = Image.new('RGB', (1280, 360 * ((len(thumbs) + 1) // 2)), '#f7f4ed')
for i, thumb in enumerate(thumbs):
    contact.paste(thumb, ((i % 2) * 640, (i // 2) * 360))
contact.save(previews / 'contact-sheet.jpg')
print(f'Static previews: {previews}')
