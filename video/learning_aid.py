"""Shared drawing and encoding for page-based learning aids.

Speech and sentence-cue timings come from the approved Q1 production workflow.
Figures carry the explanation; long reference material stays on the page.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = '#f7f4ed'; INK = '#292d29'; MUTED = '#68685f'; RUST = '#96432e'
GREEN = '#386854'; SAGE = '#e3eee6'; WASH = '#eee1d4'; LINE = '#ddd8cd'; WHITE = '#fffdf8'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
FONTS = [FONT_DIR / f for f in ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSerif.ttf')]

def font(size, bold=False, serif=False):
    return ImageFont.truetype(str(FONTS[2 if serif else int(bold)]), size)

def layer():
    im = Image.new('RGBA', (W,H), (0,0,0,0))
    return im, ImageDraw.Draw(im)

def text(d, value, x, y, size=38, width=1152, color=INK, bold=False, serif=False):
    width = min(width, W-64-x)
    f=font(size,bold,serif)
    for para in value.split('\n'):
        lines=[]; line=''
        for word in para.split():
            trial=(line+' '+word).strip()
            if d.textlength(trial,font=f)>width and line:
                lines.append(line); line=word
            else: line=trial
        lines.append(line)
        for line in lines:
            if d.textlength(line,font=f)>width+1 or y+size>H-52:
                raise ValueError(f'Text overflow: {line!r} at {x},{y}')
            d.text((x,y),line,font=f,fill=color); y+=round(size*1.28)
    return y

def header(d, chapter, title, sub=None):
    text(d,f'METADATA SYSTEMS / CHAPTER {chapter} / LEARNING AID',64,30,20,bold=True,color=RUST)
    text(d,title,64,84,44,serif=True)
    if sub: text(d,sub,64,151,28,color=MUTED)
    d.line((64,203,1216,203),fill=LINE,width=2)

def box(d,x,y,w,h,fill=WHITE,outline=LINE):
    d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=fill,outline=outline,width=2)

def arrow(d,x,y,ex,ey,color=MUTED):
    d.line((x,y,ex,ey),fill=color,width=4)
    a=math.atan2(ey-y,ex-x)
    d.polygon([(ex,ey),(ex-17*math.cos(a-.45),ey-17*math.sin(a-.45)),(ex-17*math.cos(a+.45),ey-17*math.sin(a+.45))],fill=color)

def cue(t, phrase):
    for c in t['cues']:
        if phrase.lower() in c['text'].lower(): return c['start']
    raise ValueError(f'Missing cue {phrase!r} in {t["kind"]}')

def parcel(d,x,y,color):
    d.polygon([(x,y),(x+58,y+23),(x,y+46),(x-58,y+23)],fill=WASH,outline=color,width=4)
    d.polygon([(x-58,y+23),(x,y+46),(x,y+104),(x-58,y+80)],fill=WHITE,outline=color,width=4)
    d.polygon([(x,y+46),(x+58,y+23),(x+58,y+80),(x,y+104)],fill=BG,outline=color,width=4)
    d.line((x-29,y+12,x+29,y+35,x+29,y+62),fill=color,width=3)

def parcels(d, chapter=1, y=270, selected=None, unfinished=1):
    labels=['On time','On time','Late','Unfinished'] if unfinished==1 else ['On time','Unfinished','On time','Unfinished']
    for i,(x,label) in enumerate(zip([190,490,790,1090],labels)):
        col=GREEN if label=='On time' else RUST if label=='Late' else MUTED
        if selected and i in selected:
            box(d,x-125,y-22,250,208,fill=SAGE,outline=GREEN)
        parcel(d,x,y,col)
        text(d,label,x-116,y+125,30,width=240,bold=True,color=col)

def bracket(d,n,label,y=486):
    right=920 if n==3 else 1210
    d.line((70,y-12,70,y+8,right,y+8,right,y-12),fill=GREEN,width=5)
    text(d,label,80,y+22,34,color=GREEN,bold=True)

def end_card(d,c,chapter):
    text(d,f'METADATA SYSTEMS / CHAPTER {chapter}',64,66,24,bold=True,color=RUST)
    text(d,'Try it on the page',64,160,58,serif=True)
    text(d,c.get('practice_label','Explain the example in your own words.'),64,267,38,width=1100)
    text(d,c['book_url'],64,454,32,color=RUST)
    text(d,c['attribution'],64,525,26,color=MUTED)
    text(d,'Invented example · synthetic Q1 narration',64,574,24,color=MUTED)

def render(root, make):
    root=Path(root)
    c=json.loads((root/'project.json').read_text())
    p=Path(os.environ.get('EXPLAINER_OUT',str(root.parents[1]/'out'/('q1-'+root.name)))).resolve()
    timings=json.loads((p/'timings.json').read_text())
    source_hash=hashlib.sha256(Path(__file__).read_bytes()+(root/'render.py').read_bytes()).hexdigest()
    fonts=[hashlib.sha256(f.read_bytes()).hexdigest() for f in FONTS]
    for t in timings:
        i=t['number']; dur=t['duration']
        if '--only' in sys.argv and i not in map(int,sys.argv[sys.argv.index('--only')+1].split(',')):continue
        outfile=p/f'clip-{i:02}.mp4'; stamp=outfile.with_suffix('.sha256')
        signature=hashlib.sha256(json.dumps(dict(t=t,c=c,source=source_hash,fonts=fonts),sort_keys=True).encode()).hexdigest()
        if outfile.exists() and stamp.exists() and stamp.read_text()==signature and '--force' not in sys.argv:continue
        layers=make(t,c)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',f'color=c={BG}:s={W}x{H}:r=24:d={dur}']
        filters=[]; base='0:v'
        for j,(im,start,end) in enumerate(layers):
            path=p/f'layer-{i:02}-{j}.png'; im.save(path)
            cmd+=['-loop','1','-framerate','24','-i',str(path)]
            f=f'[{j+1}:v]format=rgba,fade=t=in:st={start}:d=0.25:alpha=1'
            if end is not None:f+=f',fade=t=out:st={max(start,end-.15)}:d=0.15:alpha=1'
            filters+=[f+f'[l{j}]',f'[{base}][l{j}]overlay=0:0:shortest=1[v{j}]'];base=f'v{j}'
        filters.append(f'[{base}]format=yuv420p[out]')
        cmd+=['-filter_complex',';'.join(filters),'-map','[out]','-t',str(dur),'-an','-c:v','libx264','-crf','19','-preset','veryfast','-threads','2','-filter_complex_threads','2',str(outfile)]
        subprocess.run(cmd,check=True);stamp.write_text(signature)
        print(f'Rendered {root.name}: {t["kind"]}',flush=True)
    if '--only' in sys.argv or '--no-mux' in sys.argv:return
    (p/'clips.txt').write_text(''.join(f"file 'clip-{t['number']:02}.mp4'\n" for t in timings))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(p/'clips.txt'),'-i',str(p/'narration.wav'),'-i',str(p/'captions.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart','-metadata','title='+c['title'],'-metadata','comment=Page learning aid. Synthetic Q1 voice. Source: '+c['source_url'],str(p/(root.name+'.mp4'))],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'captions.srt'),str(p/'captions.vtt')],check=True)
    print('FINAL VIDEO READY',flush=True)
