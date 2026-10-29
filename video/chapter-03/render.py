"""Chapter-specific visuals, using the authored narration workflow's scene/mux pattern."""
from pathlib import Path
import hashlib,json,math,os,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('EXPLAINER_OUT',str(ROOT.parents[1]/'out'/'q1-chapter-03'))).resolve()
C=json.loads((ROOT/'project.json').read_text());T=json.loads((P/'timings.json').read_text())
W,H=1280,720;BG='#f7f4ed';INK='#292d29';MUTED='#68685f';RUST='#96432e';WASH='#eee1d4';GREEN='#386854';SAGE='#e3eee6';LINE='#ddd8cd';SURFACE='#fffdf8'
FD=Path(C['font_dir']);FONTS=[FD/'DejaVuSans.ttf',FD/'DejaVuSans-Bold.ttf',FD/'DejaVuSerif.ttf']
def font(size,bold=False,serif=False):return ImageFont.truetype(str(FONTS[2 if serif else 1 if bold else 0]),size)
def layer():
 im=Image.new('RGBA',(W,H),(0,0,0,0));return im,ImageDraw.Draw(im)
def text(d,s,x,y,size=34,width=1136,bold=False,serif=False,color=INK):
 width=min(width,W-64-x)
 f=font(size,bold,serif);lines=[]
 for para in s.split('\n'):
  line=''
  for word in para.split():
   test=(line+' '+word).strip()
   if d.textlength(test,font=f)>width and line:lines.append(line);line=word
   else:line=test
  lines.append(line)
 for line in lines:
  if d.textlength(line,font=f)>width+1 or y+size>H-32:raise ValueError(f'Overflow: {line} at {x},{y}')
  d.text((x,y),line,font=f,fill=color);y+=round(size*1.3)
 return y

def header(d,title,sub=None):
 text(d,'METADATA SYSTEMS  /  CHAPTER 3',64,30,18,bold=True,color=RUST)
 size=45
 while d.textlength(title,font=font(size,serif=True))>1136 and size>30:size-=1
 text(d,title,64,87,size,serif=True)
 if sub:text(d,sub,64,154,25,color=MUTED)
 d.line((64,198,1216,198),fill=LINE,width=2)
def arrow(d,x,y,ex,ey,color=MUTED):
 d.line((x,y,ex,ey),fill=color,width=3);a=math.atan2(ey-y,ex-x)
 d.polygon([(ex,ey),(ex-14*math.cos(a-.45),ey-14*math.sin(a-.45)),(ex-14*math.cos(a+.45),ey-14*math.sin(a+.45))],fill=color)
def parcel(d,cx,y,color=INK):
 # Perspective parcel; the same shape is retained across all counting scenes.
 pts=[(cx,y),(cx+65,y+25),(cx,y+51),(cx-65,y+25)]
 d.polygon(pts,fill=WASH,outline=color,width=3)
 d.polygon([(cx-65,y+25),(cx,y+51),(cx,y+116),(cx-65,y+88)],fill=SURFACE,outline=color,width=3)
 d.polygon([(cx,y+51),(cx+65,y+25),(cx+65,y+88),(cx,y+116)],fill=BG,outline=color,width=3)
 d.line((cx-32,y+13,cx+32,y+38,cx+32,y+65),fill=color,width=3)
def parcel_row(d,status=True,exclude=False,y=265):
 labels=['On time','On time','Late','Unfinished'];xs=[204,494,784,1074]
 for j,x in enumerate(xs):
  col=MUTED if exclude and j==3 else GREEN if j<2 and status else RUST if j==2 and status else INK
  parcel(d,x,y,col)
  if status:
   text(d,labels[j],x-112,y+143,27,width=240,bold=True,color=col)
   detail='arrived' if j<3 else 'not arrived'
   text(d,detail,x-112,y+185,21,width=240,color=MUTED)
  else:text(d,f'Parcel {j+1}',x-75,y+145,26,width=220,color=MUTED)
def bracket(d,n,label):
 right=918 if n==3 else 1205
 d.line((80,480,80,500,right,500,right,480),fill=GREEN,width=4)
 text(d,label,80,516,25,color=GREEN,bold=True)
def cue(t,phrase):
 for c in t['cues']:
  if phrase.lower() in c['text'].lower():return c['start']
 raise ValueError(f'Missing cue: {phrase}')
def panel(d,x,y,w,h,title,result,note):
 d.rounded_rectangle((x,y,x+w,y+h),radius=18,fill=SURFACE,outline=LINE,width=2)
 text(d,title,x+28,y+25,27,width=w-56,bold=True)
 text(d,result,x+28,y+87,62,width=w-56,serif=True,color=RUST)
 text(d,note,x+28,y+183,26,width=w-56,color=MUTED)
def building(d,x,y,house=False):
 if house:
  d.polygon([(x,y+75),(x+105,y),(x+210,y+75)],outline=GREEN,fill=SAGE,width=4)
  d.rectangle((x+22,y+75,x+188,y+190),fill=SURFACE,outline=GREEN,width=4)
  d.rectangle((x+88,y+118,x+130,y+190),outline=GREEN,width=3)
 else:
  d.rectangle((x,y+30,x+210,y+190),fill=SURFACE,outline=RUST,width=4)
  d.rectangle((x-8,y,x+218,y+30),fill=WASH,outline=RUST,width=4)
  for i in range(3):d.rectangle((x+16+i*65,y+90,x+66+i*65,y+190),outline=RUST,width=3)


# Chapter-specific scenes are inserted below.
def record(d,x,y,w,title,rows):
 h=70+len(rows)*82
 d.rounded_rectangle((x,y,x+w,y+h),radius=14,fill=SURFACE,outline=LINE,width=2)
 text(d,title,x+23,y+18,29,width=w-46,bold=True,color=RUST)
 for j,(a,b) in enumerate(rows):
  yy=y+70+j*82
  text(d,a,x+23,yy,19,width=w-46,color=MUTED)
  text(d,b,x+23,yy+28,30,width=w-46,bold=True)
 return h

def chain(d,labels,y=305,active=None):
 w=263;step=295
 for j,(a,b) in enumerate(labels):
  x=64+j*step
  d.rounded_rectangle((x,y,x+w,y+155),radius=14,fill=WASH if active==j else SURFACE,outline=RUST if active==j else LINE,width=3 if active==j else 2)
  text(d,a,x+20,y+25,23,width=w-40,bold=True,color=RUST if active==j else MUTED)
  size=28
  while d.textlength(b,font=font(size))>w-40 and size>22:size-=1
  text(d,b,x+20,y+74,size,width=w-40)
  if j<len(labels)-1:arrow(d,x+w+5,y+77,x+step-7,y+77)

def snapshot(d,y=270,selected=False):
 x=64;w=1152
 widths=[0,270,590,920]
 for j,a in enumerate(['Delivery','Promised by','Delivered at','Included?' if selected else 'Status']):text(d,a,x+widths[j]+15,y,25,bold=True,color=MUTED)
 values=[('D101','12:00','11:50','Yes'),('D102','12:00','NULL','No'),('D103','12:00','11:40','Yes'),('D104','12:00','NULL','No')]
 for i,row in enumerate(values):
  yy=y+52+i*65
  d.rounded_rectangle((x,yy,x+w,yy+58),radius=7,fill=SAGE if i in (0,2) and selected else SURFACE)
  for j,v in enumerate(row):
   if j==3 and not selected:v='Completed' if i in (0,2) else 'Unfinished'
   text(d,v,x+widths[j]+15,yy+12,27,width=[245,295,305,217][j],color=GREEN if i in (0,2) else MUTED,bold=selected and i in (0,2))

def make(t):
 k=t['kind'];layers=[]
 def add(im,start=0,end=None):layers.append((im,start,end))
 im,d=layer()
 if k=='opening':
  header(d,'Where did this number come from?','Service Analytics · completed deliveries only')
  d.rounded_rectangle((185,234,1095,572),radius=18,fill=SURFACE,outline=LINE,width=3)
  text(d,'DELIVERY PERFORMANCE',235,262,21,bold=True,color=MUTED)
  text(d,'100%',420,307,110,serif=True,color=RUST)
  text(d,'Report refreshed at 13:00 UTC',350,490,28,width=750)
  text(d,'Invented incident · 19 October 2026 · checked using SQLite',64,622,27,color=MUTED);add(im)
 elif k=='route':
  header(d,'The route to the report','Data flow: calculation and report refresh are separate steps')
  labels=[('Source','Delivery records'),('Calculation','Scheduled job'),('Stored output','Saved percentage'),('Report','Display result')]
  chain(d,labels);text(d,'Refreshing the report does not rerun the calculation.',64,548,33,bold=True,color=GREEN);add(im)
  im,d=layer();chain(d,labels,active=3);add(im,cue(t,'The report reads'))
 elif k=='distinction':
  header(d,'A route and the history of a particular result')
  boxes=[('Lineage','Records where data comes from, how it is transformed, and which datasets or reports depend on it.'),('Provenance','Records the history of a particular dataset or result: who or what created or changed it, when, and using which sources and methods.')]
  for j,(title,body) in enumerate(boxes):
   x=64+j*588;d.rounded_rectangle((x,234,x+564,582),radius=15,fill=SURFACE,outline=LINE,width=2)
   text(d,title,x+25,260,39,serif=True,color=RUST);text(d,body,x+25,328,28,width=514)
  text(d,'The terms overlap. A dependency path alone does not identify this run.',64,619,26,color=MUTED);add(im)
 elif k=='refresh':
  header(d,'Start with what the report actually read.','Report refresh · F1300')
  record(d,64,238,1152,'Refresh record',[('report_name','Delivery performance'),('refreshed_at','2026-10-19 13:00 UTC'),('output_version','summary-R1205')])
  text(d,'Follow the output identifier, not just the refresh time.',64,626,30,bold=True,color=GREEN);add(im)
  im,d=layer();d.rounded_rectangle((72,466,1208,547),radius=9,outline=RUST,width=4);add(im,cue(t,'It says'))
 elif k=='output':
  header(d,'Match the output version. Follow its run.','Investigation: references lead from the report back to its producer')
  record(d,64,234,530,'Report refresh · F1300',[('output_version','summary-R1205'),('refreshed_at','13:00 UTC')])
  record(d,662,234,554,'Published output',[('output_version','summary-R1205'),('run_id','R1205'),('published_at / percentage','12:05 UTC / 100.0')])
  arrow(d,602,351,654,351,color=RUST)
  text(d,'Published 55 minutes before the report refresh.',64,612,32,bold=True,color=GREEN);add(im)
 elif k=='run':
  header(d,'The run identifies its inputs and code.','Run record · R1205 · successful execution')
  d.rounded_rectangle((430,231,850,349),radius=14,fill=WASH,outline=RUST,width=3)
  text(d,'RUN',460,251,19,bold=True,color=MUTED);text(d,'R1205',460,281,36,bold=True)
  add(im)
  im,d=layer();record(d,64,451,540,'Retained input',[('input_snapshot_id','S1205')]);arrow(d,520,350,335,437);text(d,'read',362,384,22,color=MUTED)
  record(d,676,451,540,'Retained calculation',[('code_version','completed-v1')]);arrow(d,760,350,946,437);text(d,'executed',842,384,22,color=MUTED);add(im,cue(t,'The run record'))
 elif k=='snapshot':
  header(d,'Inspect the saved input, not today’s table.','S1205 · captured at 12:05 UTC · all four promised by noon')
  snapshot(d,y=247)
  text(d,'Here, NULL means unfinished. Assume complete records at capture.',64,619,26,color=MUTED);add(im)
 elif k=='calculation':
  header(d,'Read the retained calculation.','completed-v1 · relevant filter shown below')
  text(d,'WHERE delivered_at IS NOT NULL',64,220,29,bold=True,color=RUST)
  snapshot(d,y=278,selected=True);add(im)
  im,d=layer();text(d,'2 on time ÷ 2 completed = 100%',64,626,35,bold=True,color=GREEN);add(im,cue(t,'Two on time'))
 elif k=='recap':
  header(d,'Follow matching identifiers.','Investigation: trace the evidence behind the displayed number')
  chain(d,[('Report refresh','F1300'),('Published output','summary-R1205'),('Producing run','R1205')],y=245)
  arrow(d,720,403,690,476);arrow(d,850,403,1005,476)
  text(d,'Input: S1205',580,496,27,width=300,bold=True,color=GREEN)
  text(d,'Code:',940,496,24,width=270,color=MUTED)
  text(d,'completed-v1',940,532,26,width=275,bold=True,color=GREEN)
  text(d,'Explains 100% for those inputs.',64,483,31,width=440,bold=True)
  text(d,'Was it still current at 13:00? Chapter 4 investigates.',64,625,29,color=MUTED);add(im)
 elif k=='end':
  text(d,'METADATA SYSTEMS  /  CHAPTER 3',64,75,22,bold=True,color=RUST)
  text(d,'Where did this\nnumber come from?',64,170,65,serif=True)
  text(d,C['book_url'],64,422,34,width=1150,color=RUST)
  text(d,C['attribution'],64,515,28,color=MUTED)
  text(d,'Invented incident · synthetic narration',64,570,24,color=MUTED);add(im)
 else:raise ValueError(k)
 return layers

renderer=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
font_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in FONTS]
for t in T:
 i=t['number'];dur=t['duration'];layers=make(t)
 if '--only' in sys.argv and i not in [int(x) for x in sys.argv[sys.argv.index('--only')+1].split(',')]:continue
 outfile=P/f'clip-{i:02}.mp4';stamp=outfile.with_suffix('.sha256')
 signature=hashlib.sha256(json.dumps(dict(t=t,config=C,renderer=renderer,fonts=font_hashes),sort_keys=True).encode()).hexdigest()
 if outfile.exists() and stamp.exists() and stamp.read_text()==signature and '--force' not in sys.argv:continue
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',f'color=c={BG}:s={W}x{H}:r=24:d={dur}'];filters=[];base='0:v'
 for j,(im,start,end) in enumerate(layers):
  path=P/f'layer-{i:02}-{j}.png';im.save(path);cmd+=['-loop','1','-framerate','24','-i',str(path)]
  ff=f'[{j+1}:v]format=rgba,fade=t=in:st={start}:d=0.25:alpha=1'
  if end is not None:ff+=f',fade=t=out:st={max(start,end-.15)}:d=0.15:alpha=1'
  filters.append(ff+f'[l{j}]');filters.append(f'[{base}][l{j}]overlay=0:0:shortest=1[v{j}]');base=f'v{j}'
 filters.append(f'[{base}]format=yuv420p[out]')
 cmd+=['-filter_complex',';'.join(filters),'-map','[out]','-t',str(dur),'-an','-c:v','libx264','-crf','19','-preset','veryfast','-threads','2','-filter_complex_threads','2',str(outfile)]
 subprocess.run(cmd,check=True);stamp.write_text(signature);print(f'Rendered {i+1}/{len(T)}: {t["kind"]}',flush=True)
(P/'clips.txt').write_text(''.join(f"file 'clip-{t['number']:02}.mp4'\n" for t in T))
if '--only' not in sys.argv and '--no-mux' not in sys.argv:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'clips.txt'),'-i',str(P/'narration.wav'),'-i',str(P/'captions.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart','-metadata','title='+C['title'],'-metadata','comment=Authored chapter adaptation. Synthetic voice: '+C['voice']+'. Source: '+C['source_url'],str(P/'chapter-03.mp4')],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'captions.srt'),str(P/'captions.vtt')],check=True)
 print('FINAL VIDEO READY',flush=True)
