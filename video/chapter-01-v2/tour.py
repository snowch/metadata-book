"""Record the approved Chapter 1 demonstration with native 4K capture."""
import asyncio
CONFIG={'hold':1.5,'color_scheme':'light'}
async def tour(r):
 await r.goto('/assets/lessons/chapter-01/index.html?record',wait_for='#parcels .parcel')
 await r.pg.evaluate('document.fonts.ready')
 await r.start()
 for sid in ('task','evidence','demonstration','guided','explanation','independent','feedback','application'):
  async with r.scene(sid):
   await r.pg.evaluate('(id)=>window.showScene(id)',sid)
   # Keep the standard pointer outside the diagram while it changes.
   await r.glide(1215,680)
   await r.hold(.85)
