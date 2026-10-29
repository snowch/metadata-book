"""Check an encoded learning aid and extract evidence for visual inspection.

This verifies export integrity, captions and deliberate response pauses, not
learning effectiveness, pronunciation or human listening approval.
"""
from pathlib import Path
import argparse, hashlib, json, math, re, subprocess
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter',required=True,choices=sorted(p.name[-2:] for p in (ROOT/'video').glob('chapter-[0-9][0-9]') if (p/'project.json').is_file()))
args=parser.parse_args()
chapter=ROOT/'video'/f'chapter-{args.chapter}'
build=ROOT/'out'/f'q1-chapter-{args.chapter}'
scenes=json.loads((chapter/'narration.json').read_text())
timings=json.loads((build/'timings.json').read_text())
assert [s['text'] for s in scenes]==[s['text'] for s in timings]
assert [s['kind'] for s in scenes]==[s['kind'] for s in timings]
movie=build/f'chapter-{args.chapter}.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]))
streams=probe['streams']; v=next(s for s in streams if s['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'])==(1280,720,'24/1')
assert {s['codec_type'] for s in streams}=={'video','audio','subtitle'}
expected_duration=sum(t['duration'] for t in timings)
assert abs(float(probe['format']['duration'])-expected_duration)<.15
for stream in streams:
    if stream['codec_type'] in ('video','audio'):
        assert abs(float(stream['duration'])-expected_duration)<.15
        assert abs(float(stream.get('start_time',0)))<.05
assert timings[-1]['kind']=='end' and timings[-1]['duration']==5
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
# Compare shipped captions with canonical display narration, not speech lexicon.
blocks=re.split(r'\n\s*\n',(build/'captions.srt').read_text().strip())
caption_text=' '.join(' '.join(b.splitlines()[2:]) for b in blocks)
assert caption_text==' '.join(s['text'] for s in scenes if s['text'])
def seconds(stamp):
    h,m,s=stamp.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
previous=0; pauses=[]
for b in blocks:
    a,z=map(seconds,b.splitlines()[1].split(' --> '))
    assert a>=previous-.002 and z>a,(a,z,previous)
    previous=z
for t in timings:
    hold=t.get('hold_seconds',0)
    if hold:
        finish=max(c['end'] for c in t['cues'])
        assert t['duration']-finish>=hold,(t['kind'],t['duration'],finish)
        pauses.append(dict(kind=t['kind'],requested_seconds=hold,after_last_caption=round(t['duration']-finish,3)))
# Actual encoded frames, one per scene plus midpoint of each response hold.
frames=build/'encoded-frames';frames.mkdir(exist_ok=True)
samples=[]
for t in timings:
    at=t['start']+max(.6,t['duration']-.8)
    samples.append((t['kind'],at))
    if t.get('hold_seconds'):samples.append((t['kind']+'-response-hold',t['start']+t['duration']-t['hold_seconds']/2))
sheet=Image.new('RGB',(1280,math.ceil(len(samples)/2)*390),'white');draw=ImageDraw.Draw(sheet)
for i,(kind,at) in enumerate(samples):
    dest=frames/f'{i:02}-{kind}.jpg'
    subprocess.run(['ffmpeg','-v','error','-ss',str(at),'-i',str(movie),'-frames:v','1','-y',str(dest)],check=True)
    im=Image.open(dest)
    x=i%2*640;y=i//2*390
    sheet.paste(im.resize((640,360)),(x,y+30));draw.text((x+8,y+7),f'{kind} | {at:.2f}s',fill='black')
sheet.save(build/'encoded-contact.jpg')
# A representative dense frame at phone playback width for manual review.
Image.open(frames/f'{min(5,len(samples)-1):02}-{samples[min(5,len(samples)-1)][0]}.jpg').resize((390,219)).save(build/'phone-frame.jpg')
report=dict(chapter=args.chapter,duration=float(probe['format']['duration']),sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),bytes=movie.stat().st_size,caption_cues=len(blocks),caption_text_matches=True,decode_passed=True,pauses=pauses,human_listening_review=False,visual_review='Inspect encoded-contact.jpg and phone-frame.jpg separately')
(build/'media-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
