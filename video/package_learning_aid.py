"""Package a reviewed learning aid and refresh its page's content-versioned links.

Run verify_learning_aid.py and inspect its encoded frames and speech screening
before this step. Packaging is local; publication occurs only after merge.
"""
import argparse, hashlib, json, re, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--chapter',required=True,choices=['01','02','03']);args=ap.parse_args()
n=args.chapter;chapter=ROOT/'video'/f'chapter-{n}';build=ROOT/'out'/f'q1-chapter-{n}';dest=ROOT/'assets'/'video'/f'chapter-{n}'
config=json.loads((chapter/'project.json').read_text());media=json.loads((build/'media-verification.json').read_text());timings=json.loads((build/'timings.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert media['sha256']==sha(build/f'chapter-{n}.mp4'),'Media verification is stale'
subprocess.run(['ffmpeg','-v','error','-ss','2','-i',str(build/f'chapter-{n}.mp4'),'-frames:v','1','-y',str(build/'poster.jpg')],check=True)
dest.mkdir(exist_ok=True,parents=True)
for f in [f'chapter-{n}.mp4','captions.vtt','captions.srt','transcript.txt','poster.jpg']:shutil.copyfile(build/f,dest/f)
page=ROOT/'chapters'/Path(config['source_url']).with_suffix('.md').name
s=page.read_text();seconds=round(media['duration']);duration=f'{seconds//60} min {seconds%60:02} sec'
s=re.sub(r'(<span class="chapter-video-duration">).*?(</span>)',lambda m:m[1]+duration+m[2],s)
for f in [f'chapter-{n}.mp4','captions.vtt','transcript.txt','poster.jpg']:
    s=re.sub(re.escape(f)+r'\?v=[a-f0-9]+',f+'?v='+sha(dest/f)[:12],s)
s=re.sub(r'Download video <span>\([\d.]+ MB\)</span>',f'Download video <span>({media["bytes"]/1e6:.1f} MB)</span>',s)
s=s.replace('Watch the chapter','Practise the chapter').replace('explainer" aria-describedby','learning aid" aria-describedby')
page.write_text(s)
# Retain the standalone preview with accurate duration and page-learning purpose.
p=chapter/'watch.html';s=p.read_text();s=re.sub(r'(CHAPTER '+str(int(n))+r' · )\d+:\d+',lambda m:m[1]+f'{seconds//60}:{seconds%60:02}',s);s=s.replace('narrated explainer','narrated learning aid');p.write_text(s)
# Replace only this chapter's provenance; later chapters remain untouched.
p=ROOT/'video'/'qwen-production'/'production-manifest.json';manifest=json.loads(p.read_text());records=[]
for t in timings:
    if not t['text']:continue
    i=t['number'];meta=json.loads((build/f'raw-{i:02}.metadata.json').read_text());asr=json.loads((build/f'asr-{i:02}.json').read_text());words=json.loads((build/f'words-{i:02}.json').read_text())
    records.append(dict(scene=i,kind=t['kind'],raw_seconds=meta['seconds'],generation=meta,unprompted_asr=asr['text'],alignment=words['alignment'],hold_seconds=t.get('hold_seconds',0)))
record=dict(chapter=n,duration_seconds=media['duration'],caption_cues=media['caption_cues'],end_card_seconds=5,purpose=config['purpose'],video_sha256=media['sha256'],scenes=records)
manifest['chapters']=[record if c['chapter']==n else c for c in manifest['chapters']]
p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(chapter=n,page=str(page),duration=duration,sha256=media['sha256']),indent=2))
