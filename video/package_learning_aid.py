"""Package a reviewed learning aid and refresh its page's content-versioned links.

Run verify_learning_aid.py and inspect its encoded frames and speech screening
before this step. Packaging is local; publication occurs only after merge.
"""
import argparse, hashlib, html, json, re, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--chapter',required=True,choices=sorted(p.name[-2:] for p in (ROOT/'video').glob('chapter-[0-9][0-9]') if (p/'project.json').is_file()));args=ap.parse_args()
n=args.chapter;chapter=ROOT/'video'/f'chapter-{n}';build=ROOT/'out'/f'q1-chapter-{n}';dest=ROOT/'assets'/'video'/f'chapter-{n}'
config=json.loads((chapter/'project.json').read_text());media=json.loads((build/'media-verification.json').read_text());timings=json.loads((build/'timings.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert media['sha256']==sha(build/f'chapter-{n}.mp4'),'Media verification is stale'
subprocess.run(['ffmpeg','-v','error','-ss','2','-i',str(build/f'chapter-{n}.mp4'),'-frames:v','1','-y',str(build/'poster.jpg')],check=True)
dest.mkdir(exist_ok=True,parents=True)
for f in [f'chapter-{n}.mp4','captions.vtt','captions.srt','transcript.txt','poster.jpg']:shutil.copyfile(build/f,dest/f)
page=ROOT/'chapters'/Path(config['source_url']).with_suffix('.md').name
s=page.read_text();seconds=round(media['duration']);duration=f'{seconds//60} min {seconds%60:02} sec'
if '<figure class="chapter-video"' not in s:
    title=html.escape(config['title'],quote=True)
    note=html.escape(config.get('example_note','The example is invented. Narration uses a synthetic voice.'))
    base=f'../assets/video/chapter-{n}/'
    urls={f:base+f+'?v='+sha(dest/f)[:12] for f in [f'chapter-{n}.mp4','captions.vtt','transcript.txt','poster.jpg']}
    movie=urls[f'chapter-{n}.mp4'];poster=urls['poster.jpg'];vtt=urls['captions.vtt'];transcript=urls['transcript.txt']
    embed=f'''<figure class="chapter-video" aria-labelledby="chapter-video-title">
<figcaption id="chapter-video-title"><span>Practise the chapter</span><span class="chapter-video-duration">{duration}</span></figcaption>
<video controls playsinline preload="none" width="1280" height="720" poster="{poster}" aria-label="{title}: narrated Chapter {int(n)} learning aid" aria-describedby="chapter-video-note">
<source src="{movie}" type="video/mp4">
<track kind="captions" src="{vtt}" srclang="en" label="English">
Your browser cannot play this video. <a href="{movie}">Download the video</a> or <a href="{transcript}">read the transcript</a>.
</video>
<p class="chapter-video-note" id="chapter-video-note">{note}</p>
<p class="chapter-video-links"><a href="{transcript}">Read the transcript</a><a href="{movie}" download>Download video <span>({media['bytes']/1e6:.1f} MB)</span></a></p>
</figure>'''
    before,separator,after=s.partition('\n## ')
    if not separator:raise ValueError('No section boundary for the new chapter video')
    s=before.rstrip()+'\n\n'+embed+'\n'+separator+after
s=re.sub(r'(<span class="chapter-video-duration">).*?(</span>)',lambda m:m[1]+duration+m[2],s)
for f in [f'chapter-{n}.mp4','captions.vtt','transcript.txt','poster.jpg']:
    s=re.sub(re.escape(f)+r'\?v=[a-f0-9]+',f+'?v='+sha(dest/f)[:12],s)
s=re.sub(r'Download video <span>\([\d.]+ MB\)</span>',f'Download video <span>({media["bytes"]/1e6:.1f} MB)</span>',s)
s=s.replace('Watch the chapter','Practise the chapter').replace('explainer" aria-describedby','learning aid" aria-describedby')
page.write_text(s)
# Retain an accurate local preview for existing and newly added chapters.
p=chapter/'watch.html'
if p.exists():
    s=p.read_text();s=re.sub(r'(CHAPTER '+str(int(n))+r' · )\d+:\d+',lambda m:m[1]+f'{seconds//60}:{seconds%60:02}',s);s=s.replace('narrated explainer','narrated learning aid')
    if '<figure class="chapter-video"' in s:
        local_embed=re.search(r'<figure class="chapter-video".*?</figure>',page.read_text(),re.S)[0].replace(f'../assets/video/chapter-{n}/','')
        s=re.sub(r'<figure class="chapter-video".*?</figure>',lambda m:local_embed,s,flags=re.S)
else:
    title=html.escape(config['title'],quote=True);base=f'../assets/video/chapter-{n}/'
    local_embed=re.search(r'<figure class="chapter-video".*?</figure>',page.read_text(),re.S)[0].replace(base,'')
    s=f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Chapter {int(n)}</title>
<style>body{{margin:2rem auto;padding:0 1rem;max-width:1060px;background:#f7f4ed;color:#292d29;font:18px/1.6 system-ui}}video{{width:100%;height:auto}}figure{{margin:1rem 0}}a{{color:#96432e}}.chapter-video-duration{{margin-left:1em}}</style>
<main><h1>{title}</h1>{local_embed}<p><a href="{html.escape(config['source_url'],quote=True)}">Read Chapter {int(n)}</a></p></main></html>\n'''
p.write_text(s);shutil.copyfile(p,build/'watch.html')
# Upsert only this chapter's provenance, preserving every other chapter.
p=ROOT/'video'/'qwen-production'/'production-manifest.json';manifest=json.loads(p.read_text());records=[]
for t in timings:
    if not t['text']:continue
    i=t['number'];meta=json.loads((build/f'raw-{i:02}.metadata.json').read_text());asr=json.loads((build/f'asr-{i:02}.json').read_text());words=json.loads((build/f'words-{i:02}.json').read_text())
    records.append(dict(scene=i,kind=t['kind'],raw_seconds=meta['seconds'],generation=meta,unprompted_asr=asr['text'],alignment=words['alignment'],hold_seconds=t.get('hold_seconds',0)))
record=dict(chapter=n,duration_seconds=media['duration'],caption_cues=media['caption_cues'],end_card_seconds=5,purpose=config['purpose'],video_sha256=media['sha256'],scenes=records)
manifest['chapters']=sorted([c for c in manifest['chapters'] if c['chapter']!=n]+[record],key=lambda c:int(c['chapter']))
p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(chapter=n,page=str(page),duration=duration,sha256=media['sha256']),indent=2))
