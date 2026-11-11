"""Native browser-rendered lesson films; preserve published Q1 audio and captions.

Usage: python video/lesson_film.py --chapter 02 [--preview | --package]
Authored scene states live in chapter-NN/film.json. Recovered scene boundaries
use the original synthesis padding contract and retained speech provenance.
No TTS, resampling, speech normalization or caption retiming occurs here.
"""
from pathlib import Path
import argparse, base64, hashlib, html, json, math, re, shutil, subprocess
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'assets/lessons/chapter-01/source-sans-3.ttf'
INK, BLUE, TEAL, MUTED, AMBER, PAPER, LINE = '#172635', '#3657d6', '#087d79', '#4a6072', '#a05b08', '#fafcff', '#cbd9e6'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args): return subprocess.check_output(list(map(str,args)))
def seconds(s):
    h,m,z=s.replace(',','.').split(':'); return int(h)*3600+int(m)*60+float(z)
def captions(p):
    return [dict(start=seconds(b.splitlines()[1].split(' --> ')[0]),end=seconds(b.splitlines()[1].split(' --> ')[1]),text=' '.join(b.splitlines()[2:])) for b in re.split(r'\n\s*\n',p.read_text().strip())]

def recover(n, original, work):
    """Reconstruct exact frame boundaries without pretending raw WAVs are present."""
    manifest=json.loads((ROOT/'video/qwen-production/production-manifest.json').read_text())
    record=next(c for c in manifest['chapters'] if c['chapter']==n)
    source=json.loads((ROOT/f'video/chapter-{n}/narration.json').read_text())
    caps=captions(ROOT/f'assets/video/chapter-{n}/captions.srt')
    assert ' '.join(c['text'] for c in caps)==' '.join(s['text'] for s in source if s['text'])
    timings=[]; frame=0; ci=0
    for i,s in enumerate(source):
        if s['text']:
            meta=next(z for z in record['scenes'] if z['kind']==s['kind'])
            count=round(meta['raw_seconds']*24000)+6000+round((.45+s.get('hold_seconds',0))*24000)
            length=math.ceil(count/1000) # 24 fps, 1000 audio samples/frame
            cues=[]; joined=''
            while joined!=s['text']:
                c=caps[ci]; joined=(' '.join([joined,c['text']])).strip()
                assert s['text'].startswith(joined),s['kind']
                cues.append(dict(c,start=c['start']-frame/24,end=c['end']-frame/24));ci+=1
        else: length=120; cues=[]
        timings.append(dict(s,number=i,start=frame/24,start_frame=frame,duration=length/24,frames=length,cues=cues));frame+=length
    probe=json.loads(run('ffprobe','-v','error','-show_streams','-show_format','-of','json',original))
    v=next(z for z in probe['streams'] if z['codec_type']=='video')
    assert int(v['nb_frames'])==frame,(n,frame,v['nb_frames'])
    assert abs(float(probe['format']['duration'])-frame/24)<.15
    (work/'timings.json').write_text(json.dumps(timings,indent=2)+'\n')
    return timings,probe

def text(x,y,value,size=48,color=INK,weight=600,anchor='middle'):
    lines=str(value).split('\n')
    return ''.join(f'<text x="{x}" y="{y+i*size*1.5}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{html.escape(line)}</text>' for i,line in enumerate(lines))
def arrow(x,y,ex,ey):
    return f'<path d="M{x} {y}L{ex} {ey}" fill="none" stroke="{MUTED}" stroke-width="3" marker-end="url(#arrow)"/>'
def line(x,y,ex,ey,col=LINE):return f'<path d="M{x} {y}L{ex} {ey}" stroke="{col}" stroke-width="3"/>'
def parcel(x,y,excluded=False):
    return f'<g transform="translate({x-48},{y})" opacity="{.35 if excluded else 1}"><path d="M0 23L48 3L96 23V77L48 99L0 77ZM0 23L48 45L96 23M48 45V99M24 13L72 35V59" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round"/></g>'

def diagram(s):
    kind=s['layout']; parts=[]
    if kind=='pair':
        for x,p in zip([330,950],s['items']):
            parts.append(text(x,211,p['label'],40,MUTED))
            parts.append(text(x,309,p['value'],p.get('size',66),p.get('color',BLUE)))
            if p.get('note'):parts.append(text(x,435,p['note'],38,INK,400))
        parts.append(line(640,176,640,479))
    elif kind=='rows':
        rows=s['items'];gap=136 if len(rows)==3 else 164;y=178 if len(rows)==3 else 218
        for i,p in enumerate(rows):
            parts.append(text(82,y+i*gap,p['label'],38,MUTED,400,'start'))
            parts.append(text(82,y+72+i*gap,p['value'],p.get('size',50),p.get('color',INK),600,'start'))
            if i<len(rows)-1:parts.append(line(82,y+96+i*gap,1198,y+96+i*gap))
    elif kind=='flow':
        items=s['items'];count=len(items);span=1160/count
        for i,p in enumerate(items):
            x=60+span*(i+.5)
            parts.append(text(x,244,p['label'],38,MUTED,400))
            parts.append(text(x,326,p['value'],p.get('size',46),p.get('color',BLUE)))
            if p.get('note'):parts.append(text(x,432,p['note'],36,INK,400))
            if i<count-1:parts.append(text(x+span*.48,326,'?',52,MUTED) if s.get('uncertain') else arrow(x+span*.37,326,x+span*.59,326))
    elif kind=='parcels':
        labels=s.get('labels',['On time','On time','Late','Unfinished'])
        for i,(x,label) in enumerate(zip([202,494,786,1078],labels)):
            excluded=i in s.get('excluded',[]);parts.append(parcel(x,190+20*excluded,excluded))
            parts.append(text(x,342+20*excluded,label,40,MUTED if excluded else INK))
            if s.get('ids'):parts.append(text(x,163,s['ids'][i],36,MUTED,400))
            if s.get('times'):parts.append(text(x,440,s['times'][i],36,MUTED,400))
        if s.get('result'):parts.append(text(640,522,s['result'],s.get('result_size',64),BLUE))
    elif kind=='timeline':
        parts.append(arrow(130,307,1150,307))
        for x,p in zip([180,640,1100],s['items']):
            parts.append(line(x,288,x,326,BLUE));parts.append(text(x,252,p['value'],64,BLUE))
            parts.append(text(x,389,p['label'],38,INK,400))
        if s.get('result'):parts.append(text(640,523,s['result'],46,TEAL))
    elif kind=='statement':
        multiline=len(s['value'].split('\n'))>2
        parts.append(text(640,200 if multiline else 267,s['value'],s.get('size',76),s.get('color',BLUE)))
        if s.get('note'):parts.append(text(640,510 if multiline else 425,s['note'],44,INK,400))
    elif kind=='budget':
        parts.append(text(82,219,'Weekly maintenance',44,INK,600,'start'))
        parts.append(f'<rect x="82" y="260" width="1116" height="68" rx="4" fill="{LINE}"/><rect x="82" y="260" width="837" height="68" rx="4" fill="{TEAL}"/>')
        parts.append(text(82,389,'90 min observed',48,TEAL,600,'start'))
        parts.append(text(1198,389,'120 min limit',48,INK,600,'end'))
        parts.append(text(640,510,s.get('updates','Updates: same working day'),44,INK))
    else:raise ValueError(kind)
    if s.get('takeaway'):parts.append(text(640,552,s['takeaway'],40,TEAL))
    return ''.join(parts)

def svg(s):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-label="{html.escape(s['heading'],quote=True)}"><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0L8 4.5L0 9" fill="none" stroke="{MUTED}" stroke-width="1.3"/></marker></defs><rect width="1280" height="720" fill="{PAPER}"/>{text(640,87,s['heading'],56)}{diagram(s)}</svg>'''

def stage_frame(s,t):
    if not s.get('cue'):return 0
    matches=[c for c in t['cues'] if s['cue'].lower() in c['text'].lower()]
    if not matches:
        # A sentence may span caption chunks; map its initial characters to the first.
        joined=' '.join(c['text'] for c in t['cues']).lower();pos=joined.find(s['cue'].lower())
        assert pos>=0,(t['kind'],s['cue']);length=0
        for c in t['cues']:
            if length+len(c['text'])>pos:matches=[c];break
            length+=len(c['text'])+1
    return max(0,round(matches[0]['start']*24))

def packet_hashes(p,stream):
    return run('ffprobe','-v','error','-select_streams',stream,'-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,duration,data_hash','-of','json',p)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--chapter',required=True);ap.add_argument('--preview',action='store_true');ap.add_argument('--package',action='store_true');args=ap.parse_args();n=args.chapter
    chapter=ROOT/f'video/chapter-{n}';dest=ROOT/f'assets/video/chapter-{n}';work=ROOT/f'out/q1-chapter-{n}';work.mkdir(parents=True,exist_ok=True)
    original=work/'before-film-audit.mp4'
    if not original.exists():shutil.copyfile(dest/f'chapter-{n}.mp4',original)
    timings,probe=recover(n,original,work);film=json.loads((chapter/'film.json').read_text())
    assert list(film['scenes'])==[t['kind'] for t in timings]
    segments=[];shots=[];writer=PdfWriter();boundaries=[]
    fontdata=base64.b64encode(FONT.read_bytes()).decode()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium')
        page=browser.new_page(viewport=dict(width=1280,height=720),device_scale_factor=3)
        for t in timings:
            stages=film['scenes'][t['kind']];frames=[stage_frame(s,t) for s in stages]
            assert frames[0]==0 and frames==sorted(set(frames)),(t['kind'],frames)
            for i,s in enumerate(stages):
                name=f'{t["number"]:02}-{i:02}';art=svg(s)
                page.set_content(f'<style>@font-face{{font-family:SourceSans;src:url(data:font/ttf;base64,{fontdata})}}*{{box-sizing:border-box}}body{{margin:0;width:1280px;height:720px;font-family:SourceSans,sans-serif}}svg{{display:block}}@page{{size:1280px 720px;margin:0}}</style>'+art)
                page.evaluate('document.fonts.ready')
                boxes=page.locator('text').evaluate_all('(els)=>els.map(e=>({text:e.textContent,...Object.fromEntries(["x","y","width","height"].map(k=>[k,e.getBBox()[k]]))}))')
                for b in boxes:assert b['x']>=40 and b['x']+b['width']<=1240 and b['y']>=20 and b['y']+b['height']<=576,(n,t['kind'],b)
                for j,a in enumerate(boxes):
                    for b in boxes[j+1:]:
                        assert min(a['x']+a['width'],b['x']+b['width'])<=max(a['x'],b['x']) or min(a['y']+a['height'],b['y']+b['height'])<=max(a['y'],b['y']),(n,t['kind'],'Overlapping labels',a,b)
                shot=work/f'film-{name}.png';page.screenshot(path=str(shot));shots.append((t['kind'],s,shot))
                pdf=work/f'film-{name}.pdf';page.pdf(path=str(pdf),width='1280px',height='720px',print_background=True,prefer_css_page_size=True)
                writer.add_page(PdfReader(pdf).pages[0])
                end=frames[i+1] if i+1<len(frames) else t['frames'];assert end>frames[i]
                segments.append((shot,(end-frames[i])/24))
                boundaries.append(dict(scene=t['kind'],stage=i,start_frame=t['start_frame']+frames[i],frames=end-frames[i],heading=s['heading'],cue=s.get('cue')))
        browser.close()
    writer.write(work/'deck.pdf')
    sheet=Image.new('RGB',(1280,math.ceil(len(shots)/2)*390),'white');d=ImageDraw.Draw(sheet)
    for i,(kind,s,path) in enumerate(shots):
        x=i%2*640;y=i//2*390;sheet.paste(Image.open(path).resize((640,360)),(x,y+30));d.text((x+8,y+7),f'{kind} / {s.get("cue","scene start")}',fill='black')
    sheet.save(work/'film-preview.jpg')
    if args.preview:print(work/'film-preview.jpg');return
    concat=work/'film-concat.txt';concat.write_text(''.join(f"file '{p}'\nduration {duration:.9f}\n" for p,duration in segments)+f"file '{segments[-1][0]}'\n")
    duration=sum(t['frames'] for t in timings)/24;silent=work/f'chapter-{n}-silent.mp4';movie=work/f'chapter-{n}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=24,format=yuv420p','-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-movflags','+faststart',str(silent)],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(original),'-map','0:v','-map','1:a','-map','1:s','-c','copy','-movflags','+faststart',str(movie)],check=True)
    for stream in ('a','s'):assert packet_hashes(original,stream)==packet_hashes(movie,stream),stream
    final=json.loads(run('ffprobe','-v','error','-show_streams','-of','json',movie));v=next(s for s in final['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(3840,2160,'24/1',round(duration*24))
    # Existing verifier also checks decoded audio/captions and actual question holds.
    for f in ('captions.srt','captions.vtt','transcript.txt'):shutil.copyfile(dest/f,work/f)
    report=dict(chapter=n,workflow='Native browser states synchronized to retained Q1 timeline',visual_parent_sha=sha(original),audio_packets_unchanged=True,subtitle_packets_unchanged=True,duration_seconds=duration,native_dimensions=[3840,2160],fps=24,control_safe_area_px=144,stages=boundaries,assets={f.name:dict(sha256=sha(f),bytes=f.stat().st_size) for f in [movie,silent,work/'deck.pdf']},human_listening_review=False,learning_outcomes='Not measured')
    (chapter/'film-production.json').write_text(json.dumps(report,indent=2)+'\n')
    subprocess.run([str(Path(__import__('sys').executable)),str(ROOT/'video/verify_learning_aid.py'),'--chapter',n],check=True)
    if args.package:package(n,chapter,dest,work,report)
    print('Ready',n,duration,'audio and subtitle packets unchanged',flush=True)

def package(n,chapter,dest,work,report):
    run('ffmpeg','-v','error','-y','-ss','2','-i',work/f'chapter-{n}.mp4','-frames:v','1','-vf','scale=1280:720',work/'poster.jpg')
    for f in (f'chapter-{n}.mp4',f'chapter-{n}-silent.mp4','deck.pdf','poster.jpg'):shutil.copyfile(work/f,dest/f)
    config=json.loads((chapter/'project.json').read_text());page=ROOT/'chapters'/Path(config['source_url']).with_suffix('.md').name;s=page.read_text()
    for f in (f'chapter-{n}.mp4','poster.jpg'):s=re.sub(re.escape(f)+r'\?v=[a-f0-9]+',f+'?v='+sha(dest/f)[:12],s)
    s=re.sub(r'Download video <span>\([\d.]+ MB\)</span>',f'Download video <span>({(dest/f"chapter-{n}.mp4").stat().st_size/1e6:.1f} MB)</span>',s)
    s=s.replace('width="1280" height="720" poster=','width="3840" height="2160" poster=')
    links=f'<p class="chapter-video-links"><a href="../assets/video/chapter-{n}/deck.pdf?v={sha(dest/"deck.pdf")[:12]}">Download the slide deck</a><a href="../assets/video/chapter-{n}/chapter-{n}-silent.mp4?v={sha(dest/f"chapter-{n}-silent.mp4")[:12]}" download>Download the silent master</a></p>'
    if 'Download the slide deck' in s:s=re.sub(r'<p class="chapter-video-links">[^\n]*Download the slide deck[^\n]*</p>',lambda _:links,s)
    else:s=s.replace('</figure>',links+'\n</figure>',1)
    page.write_text(s)
    preview=chapter/'watch.html';local=re.search(r'<figure class="chapter-video".*?</figure>',s,re.S)[0].replace(f'../assets/video/chapter-{n}/','')
    old=preview.read_text();old=re.sub(r'<figure class="chapter-video".*?</figure>',lambda _:local,old,flags=re.S);preview.write_text(old)
    path=ROOT/'video/qwen-production/production-manifest.json';m=json.loads(path.read_text());r=next(c for c in m['chapters'] if c['chapter']==n)
    r['video_sha256']=sha(dest/f'chapter-{n}.mp4');r['picture_workflow']='Browser-rendered native 4K states; unchanged Q1 audio/subtitle packets';r['picture_provenance']=f'video/chapter-{n}/film-production.json'
    path.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':main()
