"""Rebuild picture and PDF only, preserving the published audio and caption packets.

Run against the repository served at http://127.0.0.1:8031. Uses the retained
capture timeline and independent ASR anchors in out/chapter-01-v2/audio/.
"""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'out/chapter-01-v2';DEST=ROOT/'assets/video/chapter-01-v2'
config=json.loads((Path(__file__).parent/'visuals.json').read_text());scenes=json.loads((Path(__file__).parent/'scenes.json').read_text());tl=json.loads((W/'timeline.json').read_text())
original=W/'before-simplification.mp4'
if not original.exists():shutil.copyfile(DEST/'chapter-01.mp4',original)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(original)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');frames=int(v['nb_frames']);duration=frames/30
starts=[round((s['t']-tl['start'])*30) for s in tl['scenes']];starts[0]=0;bounds=starts+[frames]
def norm(s):
 s=re.sub('[^a-z0-9]','',s.lower());return {'2':'two'}.get(s,s)
def reveal_time(sid):
 phrase=config[sid].get('calculation_phrase')
 if not phrase:return None
 words=json.loads((W/'audio'/f'{sid}.asr.json').read_text())['words']
 for i in range(len(words)-len(phrase)+1):
  if [norm(w['text']) for w in words[i:i+len(phrase)]]==phrase:return round(words[i]['start']*30)
 raise ValueError(f'Missing calculation cue for {sid}')
shots=W/'simplified-frames';shots.mkdir(exist_ok=True);segments=[];samples=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium')
 page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=3)
 page.goto('http://127.0.0.1:8031/assets/lessons/chapter-01/index.html?record');page.evaluate('document.fonts.ready')
 for i,scene in enumerate(scenes):
  sid=scene['id'];length=bounds[i+1]-bounds[i];reveal=reveal_time(sid)
  page.evaluate('()=>document.getAnimations().forEach(a=>a.finish())')
  page.evaluate('([id,heading])=>setRecordingScene(id,heading)',[sid,config[sid]['heading']])
  page.evaluate('()=>{window.transitions=document.getAnimations();transitions.forEach(a=>{a.pause();a.currentTime=0})}')
  events=sorted(set([0,8,15,24]+([reveal] if reveal is not None else [])))
  events=[e for e in events if e<length]
  for n,event in enumerate(events):
   page.evaluate('(ms)=>transitions.forEach(a=>{a.currentTime=ms})',event/30*1000)
   if reveal is not None and event>=reveal:page.evaluate('revealCalculation()')
   assert page.evaluate('document.documentElement.scrollHeight===720')
   # Every meaningful visual remains above the bottom 144px control/caption area.
   assert page.locator('.result').bounding_box()['y']+page.locator('.result').bounding_box()['height']<=576
   shot=shots/f'{i:02}-{n:02}.png';page.screenshot(path=str(shot))
   finish=events[n+1] if n+1<len(events) else length
   segments.append((shot,(finish-event)/30))
  samples.append(dict(id=sid,start_frame=bounds[i],frames=length,calculation_frame=reveal))
 browser.close()
manifest=W/'simplified-concat.txt';manifest.write_text(''.join(f"file '{path}'\nduration {seconds:.9f}\n" for path,seconds in segments)+f"file '{segments[-1][0]}'\n")
silent=DEST/'chapter-01-silent.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-vf','fps=30,format=yuv420p','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-movflags','+faststart',str(silent)],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(original),'-map','0:v','-map','1:a','-map','1:s','-c','copy','-movflags','+faststart',str(DEST/'chapter-01.mp4')],check=True)
def packets(path,selector):
 return subprocess.check_output(['ffprobe','-v','error','-select_streams',selector,'-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,duration,data_hash','-of','json',str(path)])
for selector in ('a','s'):assert packets(original,selector)==packets(DEST/'chapter-01.mp4',selector),selector
new=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(DEST/'chapter-01.mp4')]))
newv=next(s for s in new['streams'] if s['codec_type']=='video');assert int(newv['nb_frames'])==frames
(W/'visual-only-verification.json').write_text(json.dumps(dict(frames=frames,duration=duration,audio_packets_unchanged=True,caption_packets_unchanged=True,control_safe_area_px=144,scenes=samples),indent=2)+'\n')
print('Visual replacement ready; audio/caption packet payloads and timestamps unchanged.',flush=True)
