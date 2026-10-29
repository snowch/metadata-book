"""Exercise a packaged learning aid in Chromium at desktop and phone widths."""
import argparse,json,re
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--chapter',required=True,choices=['01','02','03']);args=ap.parse_args()
n=args.chapter;build=ROOT/'out'/f'q1-chapter-{n}'
c=json.loads((ROOT/'video'/f'chapter-{n}'/'project.json').read_text());timings=json.loads((build/'timings.json').read_text())
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        # Chromium seeks with byte ranges; the standard Python server omits them.
        path=Path(self.translate_path(self.path))
        if path.suffix!='.mp4' or not path.is_file():return super().do_GET()
        data=path.read_bytes();size=len(data);start=0;end=size-1
        match=re.fullmatch(r'bytes=(\d+)-(\d*)',self.headers.get('Range',''))
        if match:
            start=int(match[1]);end=min(int(match[2]) if match[2] else end,end)
            if start> end:
                self.send_error(416);return
        self.send_response(206 if match else 200)
        self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes')
        if match:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length',str(end-start+1));self.end_headers()
        try:self.wfile.write(data[start:end+1])
        except (BrokenPipeError,ConnectionResetError):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'_site')))
Thread(target=server.serve_forever,daemon=True).start()
errors=[];checks=[]
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width in [960,390]:
        page=browser.new_page(viewport=dict(width=width,height=950));page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}/chapters/'+Path(c['source_url']).name)
        video=page.locator('video');video.scroll_into_view_if_needed()
        assert video.get_attribute('controls') is not None
        assert video.get_attribute('autoplay') is None
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        video.evaluate('(v)=>{v.muted=true;v.preload="auto";v.load()}')
        page.wait_for_function('document.querySelector("video").readyState>=2')
        page.wait_for_function('document.querySelector("video").textTracks.length===1')
        video.evaluate('(v)=>{v.textTracks[0].mode="showing"}')
        page.wait_for_function('document.querySelector("track").readyState===2')
        assert abs(video.evaluate('(v)=>v.duration')-sum(t['duration'] for t in timings))<.15
        video.evaluate('(v)=>v.play()')
        page.wait_for_function('document.querySelector("video").currentTime>.4')
        video.evaluate('(v)=>v.pause()')
        for t in timings:
            if not t.get('hold_seconds'):continue
            target=t['start']+t['duration']-t['hold_seconds']/2
            video.evaluate('(v,t)=>{v.currentTime=t}',target)
            page.wait_for_function('(t)=>Math.abs(document.querySelector("video").currentTime-t)<.1 && !document.querySelector("video").seeking',arg=target)
            assert video.evaluate('(v)=>v.textTracks[0].activeCues.length')==0,'Caption leaked into response hold'
            video.screenshot(path=str(build/f'browser-{width}-{t["kind"]}.png'))
        # Practice return target exists and example-record UI loads.
        page.locator('.reader-action a').first.click();page.wait_for_selector('.metadata-map.is-ready')
        page.locator('button[data-pane="example"]').click()
        assert page.locator('.map-detail h2').inner_text()
        checks.append(dict(width=width,playback=True,seeking=True,captions=True,response_holds=True,map_exercise=True))
        page.close()
    browser.close()
 assert not errors,errors
 (build/'browser-verification.json').write_text(json.dumps(dict(checks=checks,page_errors=errors),indent=2)+'\n')
 print(json.dumps(checks))
finally:server.shutdown()
