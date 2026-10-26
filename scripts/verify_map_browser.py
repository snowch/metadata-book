"""Browser checks for the metadata map. Build first; requires Playwright + Chromium."""

from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright, expect
import json
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
ROOT = Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT / '_site')))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
data=json.loads((ROOT / 'assets/metadata-map.json').read_text())
GEOMETRY_CHECK = r"""() => {
 const svg=document.querySelector('.map-connections'),canvas=document.querySelector('.map-canvas');
 const bounds=canvas.getBoundingClientRect(),scale=bounds.width/canvas.offsetWidth;
 const box=el=>{const r=el.getBoundingClientRect();return {left:(r.left-bounds.left)/scale,right:(r.right-bounds.left)/scale,top:(r.top-bounds.top)/scale,bottom:(r.bottom-bounds.top)/scale}};
 const cards=[...canvas.querySelectorAll('.map-focus-node')].map(el=>({id:el.dataset.focusNode,...box(el)}));
 const labels=[...svg.querySelectorAll('.map-connection-label')].map(el=>({from:el.dataset.from,to:el.dataset.to,...box(el)}));
 const inside=(p,r)=>p.x>r.left+.2&&p.x<r.right-.2&&p.y>r.top+.2&&p.y<r.bottom-.2;
 const overlap=(a,b)=>a.left<b.right-.2&&a.right>b.left+.2&&a.top<b.bottom-.2&&a.bottom>b.top+.2;
 const onBoundary=(p,r)=>p.x>=r.left-.3&&p.x<=r.right+.3&&p.y>=r.top-.3&&p.y<=r.bottom+.3&&!inside(p,r);
 const paths=[...svg.querySelectorAll('.map-connection')],samples=[],problems=[];
 for(const path of paths){
  const length=path.getTotalLength(),points=[];
  for(let t=0;t<=length;t+=2){
   const point=path.getPointAtLength(t);points.push(point);
   for(const card of cards)if(inside(point,card))problems.push('path enters '+card.id);
   for(const label of labels)if((label.from!==path.dataset.from||label.to!==path.dataset.to)&&inside(point,label))problems.push('path enters another label');
  }
  points.push(path.getPointAtLength(length));samples.push(points);
  if(!onBoundary(points[0],cards.find(c=>c.id===path.dataset.from)))problems.push('wrong source');
  if(!onBoundary(points[points.length-1],cards.find(c=>c.id===path.dataset.to)))problems.push('wrong target');
 }
 const orient=(a,b,c)=>(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);
 for(let i=0;i<samples.length;i++)for(let j=i+1;j<samples.length;j++){
  const a=samples[i],b=samples[j];
  for(let x=1;x<a.length;x++)for(let y=1;y<b.length;y++){
   if(orient(a[x-1],a[x],b[y-1])*orient(a[x-1],a[x],b[y])<-.001&&orient(b[y-1],b[y],a[x-1])*orient(b[y-1],b[y],a[x])<-.001)problems.push('arrows cross');
  }
 }
 for(const label of labels)for(const obstacle of [...cards,...labels.filter(other=>other!==label)])if(overlap(label,obstacle))problems.push('label overlap');
 return {paths:paths.length,labels:labels.length,problems};
}"""
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':1440,'height':1100})
 page.on('pageerror',lambda e:errors.append(str(e)))
 for chapter in data['chapters']:
  page.goto(base+chapter['href'])
  assert page.locator('.book-sidebar').count()==1
  assert page.locator('.header-map').get_attribute('href')==f'../metadata-map.html?chapter={chapter["number"]}'
  page.locator('.header-map').click()
  page.wait_for_selector('.metadata-map.is-ready')
  assert page.locator('.book-sidebar').count()==0
  assert page.locator('.book-layout').evaluate('(el)=>getComputedStyle(el).display')=='block'
  assert page.locator('#map-chapter-filter').input_value()==str(chapter['number'])
  assert page.locator('.map-return').get_attribute('href')==chapter['href']
 page.goto(base+'chapters/05-collecting-metadata.html')
 assert page.locator('.header-map').get_attribute('href')=='../metadata-map.html?chapter=5'
 page.locator('.header-map').click()
 page.wait_for_selector('.metadata-map.is-ready')
 assert page.locator('#map-chapter-filter').input_value()=='5'
 assert 'Chapter 5' in page.locator('.map-return').inner_text()
 assert page.locator('.map-detail h2').inner_text()=='Source observation'
 page.locator('#map-chapter-filter').select_option('3')
 assert 'chapter=5' in page.url and 'focus=3' in page.url
 assert page.locator('.map-detail h2').inner_text()=='Report refresh'
 page.locator('.map-detail [data-record-target="published-output"]').first.click()
 assert page.locator('.map-detail h2').inner_text()=='Published output'
 page.locator('.map-detail [data-record-target="run"]').first.click()
 assert page.locator('.map-detail h2').inner_text()=='Run'
 page.locator('[data-tab="fields"]').click()
 assert page.locator('.map-detail .map-fields-panel').is_visible()
 page.locator('[data-tab="fields"]').press('ArrowLeft')
 assert page.locator('[data-tab="example"]').get_attribute('aria-selected')=='true'
 page.reload();page.wait_for_selector('.metadata-map.is-ready')
 assert page.locator('.map-detail h2').inner_text()=='Run'
 assert 'Chapter 5' in page.locator('.map-return').inner_text()
 for record in data['records']:
  page.locator(f'[data-select-record="{record["id"]}"]').click()
  assert page.locator('.map-detail h2').inner_text()==record['label']
  assert page.locator('.map-detail .map-example-values > div').count()==len(record['fields'])
  page.locator('[data-tab="fields"]').click()
  assert page.locator('.map-detail tbody tr').count()>=len(record['fields'])
  expected_edges=[e for e in data['relationships'] if record['id'] in (e['from'],e['to'])]
  expect(page.locator('.map-connection')).to_have_count(len(expected_edges))
  actual=page.locator('.map-connection').evaluate_all('(els)=>els.map(el=>[el.dataset.from,el.dataset.to])')
  assert sorted(actual)==sorted([[e['from'],e['to']] for e in expected_edges])
  connected={record['id']}|{e[k] for e in expected_edges for k in ('from','to')}
  assert page.locator('.map-focus-node').count()==len(connected)
  assert page.locator('.map-overview .map-node').count()==15
  geometry=page.evaluate(GEOMETRY_CHECK)
  assert geometry['labels']==len(expected_edges) and not geometry['problems'],(record['id'],geometry)
 for chapter in data['chapters']:
  page.locator('#map-chapter-filter').select_option(str(chapter['number']))
  expected=sum(any(c['number']==chapter['number'] for c in r['chapters']) for r in data['records'])
  assert page.locator('.map-node.is-chapter').count()==expected
 page.locator('#map-chapter-filter').select_option('all')
 assert page.locator('.map-node.is-chapter').count()==0
 page.locator('.map-return').click();assert page.url==base+'chapters/05-collecting-metadata.html'
 for width in (320,390,768,900,1024,1440):
  for scheme in ('light','dark'):
   page.set_viewport_size({'width':width,'height':1100});page.emulate_media(color_scheme=scheme)
   page.goto(base+'metadata-map.html?chapter=4');page.wait_for_selector('.metadata-map.is-ready')
   assert page.locator('.metadata-map').get_attribute('data-view')==('list' if width<=700 else 'map')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,scheme)
   assert page.locator('.header-map').is_visible()
   page.evaluate('document.fonts.ready')
   if width >= 768:
    assert page.locator('.map-canvas').bounding_box()['height'] < 850,(width,'compact overview')
   page.locator('button[data-view="map"]').click()
   page.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
   initial_zoom=int(page.locator('.map-zoom-value').inner_text().rstrip('%'))
   page.locator('[data-zoom="in"]').click();expect(page.locator('.map-zoom-value')).to_have_text(f'{initial_zoom+10}%')
   page.locator('[data-zoom="out"]').click();expect(page.locator('.map-zoom-value')).to_have_text(f'{initial_zoom}%')
   page.locator('[data-zoom="fit"]').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'zoom')
   page.locator('[data-select-record="report-refresh"]').press('Enter')
   assert page.locator('.map-detail h2').inner_text()=='Report refresh'
   if width < 1200:
    assert page.locator('.map-explorer').is_visible()
    assert not page.locator('.map-detail').is_visible()
    zoom=page.locator('.map-zoom-value').inner_text()
    page.locator('.map-viewport').evaluate('(el)=>el.scrollLeft=25')
    scroll_left=page.locator('.map-viewport').evaluate('(el)=>el.scrollLeft')
    page.locator('.map-view-record').click()
    expect(page.locator('.map-detail h2')).to_be_focused()
    assert page.locator('.map-detail').is_visible()
    assert not page.locator('.map-explorer').is_visible()
    assert 'panel=details' in page.url
    page.locator('.map-back-to-records').click()
    expect(page.locator('[data-focus-record="report-refresh"]')).to_be_focused()
    assert page.locator('.map-zoom-value').inner_text()==zoom
    assert page.locator('.map-viewport').evaluate('(el)=>el.scrollLeft')==scroll_left
    page.locator('button[data-pane="map"]').press('ArrowRight')
    expect(page.locator('button[data-pane="details"]')).to_be_focused()
    assert page.locator('.map-detail').is_visible()
    page.reload();page.wait_for_selector('.metadata-map.is-ready')
    assert page.locator('.map-detail').is_visible()
    page.locator('button[data-pane="details"]').press('Home')
    expect(page.locator('button[data-pane="map"]')).to_be_focused()
    assert page.locator('.map-explorer').is_visible()
   else:
    assert not page.locator('.map-section-tabs').is_visible()
    assert page.locator('.map-detail').is_visible()
    assert page.locator('.map-explorer').is_visible()
   page.locator('[data-select-record="dataset"]').click()
   expect(page.locator('.map-connection')).to_have_count(7)
   geometry=page.evaluate(GEOMETRY_CHECK)
   assert geometry['labels']==7 and not geometry['problems'],(width,scheme,geometry)
   assert page.locator('.map-canvas').evaluate('(el)=>el.offsetHeight')<=650
   page.locator('[data-focus-record="column"]').click()
   assert page.locator('.map-selection-label').inner_text()=='Column'
   assert page.locator('.map-focus-node').count()==2
   page.goto(base+'index.html')
   assert page.locator('.reader-action').is_visible()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'contents')
   page.locator('.reader-action a').click()
   page.wait_for_selector('.metadata-map.is-ready')
   assert page.locator('#map-chapter-filter').input_value()=='all'
 page.goto(base+'metadata-map.html#record-column')
 page.wait_for_selector('.metadata-map.is-ready')
 assert page.locator('.map-detail h2').inner_text()=='Column'
 assert 'record=column' in page.url and '#record-' not in page.url
 page.goto(base+'metadata-map.html?record=report-refresh')
 page.wait_for_selector('.metadata-map.is-ready')
 page.locator('.map-detail [data-record-target="published-output"]').first.focus()
 page.keyboard.press('Enter')
 expect(page.locator('.map-detail h2')).to_be_focused()
 page.goto(base+'metadata-map.html?chapter=999&focus=bad&record=%3Cscript%3E&view=no')
 page.wait_for_selector('.metadata-map.is-ready')
 assert page.locator('#map-chapter-filter').input_value()=='all'
 assert not page.locator('.map-return').is_visible()
 page.locator('[data-select-record="published-output"]').click()
 edges=page.locator('.map-relationship-summary li')
 produced=edges.filter(has=page.locator('.map-relationship-verb',has_text='produced by'))
 assert produced.locator('a').all_text_contents()==['Published output','Run']
 page.locator('.map-relationship-text > summary').click()
 produced.locator('a').last.click()
 assert page.locator('.map-detail h2').inner_text()=='Run'
 page.emulate_media(media='print')
 assert page.locator('.map-fallback').is_visible()
 page.close()
 nojs=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
 nojs.goto(base+'metadata-map.html')
 assert nojs.locator('.map-fallback-record').count()==15
 assert nojs.locator('#record-report-refresh').is_visible()
 assert nojs.evaluate('document.documentElement.scrollWidth<=innerWidth')
 nojs.locator('[data-select-record="report-refresh"]').click()
 assert nojs.url.endswith('#record-report-refresh')
 browser.close()
server.shutdown()
assert not errors,errors
print('Map interaction, linked records, tabs/keyboard, all chapters, origin return, URL reload, 12 viewport/theme combinations, invalid parameters, print and no-JS fallback passed.')
