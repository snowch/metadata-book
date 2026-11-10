"""Record the approved Chapter 1 demonstration with native 4K capture."""
import asyncio,json,time
from pathlib import Path
VISUALS=json.loads((Path(__file__).resolve().parents[2]/'video/chapter-01-v2/visuals.json').read_text())
CONFIG={'hold':1.5,'color_scheme':'light'}
async def tour(r):
 await r.goto('/assets/lessons/chapter-01/index.html?record',wait_for='#parcels .parcel')
 await r.pg.evaluate('document.fonts.ready')
 await r.start()
 for sid in ('task','evidence','demonstration','guided','explanation','independent','feedback','application'):
  async with r.scene(sid):
   at=time.monotonic()
   await r.pg.evaluate('([id,heading])=>setRecordingScene(id,heading)',[sid,VISUALS[sid]['heading']])
   # Keep the standard pointer outside the diagram while it changes.
   await r.glide(1215,680)
   if 'calculation_seconds' in VISUALS[sid]:
    await r.hold(max(0,VISUALS[sid]['calculation_seconds']-(time.monotonic()-at)))
    await r.pg.evaluate('revealCalculation()')
   else:
    await r.hold(.85)
