from playwright.sync_api import sync_playwright
from pathlib import Path
from pypdf import PdfWriter
root=Path(__file__).resolve().parents[2];out=root/'out/chapter-01-v2';scenes=__import__('json').loads((out/'scenes.json').read_text());out.joinpath('slides').mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium')
 page=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=3)
 page.goto('http://127.0.0.1:8031/assets/lessons/chapter-01/index.html?record');page.evaluate('document.fonts.ready');writer=PdfWriter()
 for i,s in enumerate(scenes,1):
  visual=__import__('json').loads((root/'video/chapter-01-v2/visuals.json').read_text())[s['id']]
  page.evaluate('([id,heading])=>setRecordingScene(id,heading)',[s['id'],visual['heading']])
  if 'calculation_phrase' in visual:page.evaluate('revealCalculation()')
  page.wait_for_timeout(900)
  assert page.evaluate('document.documentElement.scrollHeight<=720'),s['id']
  page.screenshot(path=str(out/'slides'/f's-{i:02}.png'))
  path=out/'slides'/f's-{i:02}.pdf';page.pdf(path=str(path),width='1280px',height='720px',print_background=True);writer.append(str(path))
 writer.write(str(out/'chapter-01-deck.pdf'))
 for width in (390,960):
  page.set_viewport_size({'width':width,'height':950});page.goto('http://127.0.0.1:8031/assets/lessons/chapter-01/index.html');page.evaluate('document.fonts.ready')
  page.get_by_role('button',name='Completed deliveries',exact=True).click();assert page.locator('#percentage').inner_text()=='66.7%'
  page.get_by_role('button',name='All parcels due',exact=True).click();assert page.locator('#percentage').inner_text()=='50.0%'
  page.get_by_role('button',name='Try six parcels').click();assert page.locator('#percentage').inner_text()=='?'
  page.locator('#answer').fill('4');page.get_by_role('button',name='Check my answer').click();assert 'Four counts only completed' in page.locator('#feedback').inner_text();assert page.locator('#percentage').inner_text()=='33.3%'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  page.screenshot(path=str(out/f'lab-{width}.png'),full_page=True)
 b.close()
print('Deck export and phone/desktop lab interactions passed')
