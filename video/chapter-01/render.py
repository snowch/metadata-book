"""Chapter-specific visuals, using the authored narration workflow's scene/mux pattern."""
from pathlib import Path
import hashlib,json,math,os,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('EXPLAINER_OUT',str(ROOT.parents[1]/'out'/'chapter-01'))).resolve()
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
 text(d,'METADATA SYSTEMS  /  CHAPTER 1',64,30,18,bold=True,color=RUST)
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

def make(t):
 k=t['kind'];layers=[]
 def add(im,start=0,end=None):layers.append((im,start,end))
 im,d=layer()
 if k in ('opening','completed','due'):
  header(d,{'opening':'Four parcels. What does “on time” mean?','completed':'Of completed deliveries, how many were on time?','due':'Of all deliveries due, how many arrived on time?'}[k], 'All four promised by noon · measured at 13:00 UTC')
  if k=='opening':
   parcel_row(d,status=False);text(d,'Invented example · assume complete records at 13:00',64,625,25,color=MUTED);add(im,0,cue(t,'At one'))
   im,d=layer();header(d,'Four parcels. What does “on time” mean?','All four promised by noon · measured at 13:00 UTC');parcel_row(d);text(d,'2 on time  +  1 late  +  1 unfinished',205,540,35,bold=True);text(d,'Invented example · assume complete records at 13:00',64,625,25,color=MUTED);add(im,cue(t,'At one'))
  else:
   parcel_row(d,exclude=k=='completed');add(im)
   im,d=layer();bracket(d,3 if k=='completed' else 4,'3 completed deliveries' if k=='completed' else '4 deliveries due');add(im,cue(t,'Three parcels' if k=='completed' else 'All four parcels'))
   im,d=layer();text(d,'2 of 3 = 66.7%' if k=='completed' else '2 of 4 = 50.0%',80,570,55,bold=True,color=RUST);add(im,cue(t,'Two out of'))
 elif k in ('compare','owner'):
  header(d,'Same records. Different questions.' if k=='compare' else 'A definition makes the decision visible.')
  panel(d,64,240,550,300,'Completed deliveries' if k=='compare' else 'Another team: completed','2 of 3 = 66.7%','Unfinished deliveries excluded')
  panel(d,640,240,576,300,'All deliveries due' if k=='compare' else 'Delivery Operations: all due','2 of 4 = 50.0%','Unfinished deliveries included')
  text(d,'Both valid for their stated questions.' if k=='compare' else 'Name the team that can explain the definition.',64,596,33,bold=True,color=GREEN);add(im)
 elif k=='metadata':
  header(d,'Metadata describes data.')
  text(d,'Information that describes data:\nits structure, meaning, origin and use.',64,233,39,width=1120,serif=True)
  for j,(a,b) in enumerate([('STRUCTURE','Column names\nand types'),('MEANING','A metric’s\ndefinition'),('ORIGIN','The job that\nproduced it')]):
   x=64+j*389;d.rounded_rectangle((x,400,x+365,601),radius=15,fill=SURFACE,outline=LINE,width=2);text(d,a,x+24,423,19,bold=True,color=RUST);text(d,b,x+24,469,29,width=315)
  add(im)
 elif k=='definition':
  header(d,'Write down the decision.','Metric definition · Delivery Operations')
  rows=[('Measure','Percentage of deliveries due that arrived on time'),('On time','Delivered at or before the promised time'),('Denominator','All due by noon, including unfinished deliveries'),('Measured at','13:00 UTC on the reporting date'),('Responsible team','Delivery Operations'),('Source','deliveries table')]
  for j,(a,b) in enumerate(rows):
   y=224+j*66
   d.rounded_rectangle((64,y,1216,y+58),radius=8,fill=WASH if j==2 else SURFACE)
   text(d,a,80,y+14,23,width=250,bold=True,color=RUST if j==2 else MUTED);text(d,b,354,y+14,25,width=842,bold=j==2)
  add(im)
  im,d=layer();d.rounded_rectangle((64,356,1216,414),radius=8,outline=RUST,width=4);add(im,cue(t,'Include every'))
 elif k=='field':
  header(d,'A field name is not a complete meaning.','delivered_at')
  building(d,222,284);building(d,850,284,True)
  text(d,'Depot arrival?',150,515,36,width=460,serif=True);text(d,'Customer arrival?',762,515,36,width=480,serif=True)
  text(d,'Two possible meanings. Check the definition.',64,620,30,color=MUTED)
  arrow(d,640,235,330,265);arrow(d,640,235,955,265);add(im)
 elif k=='mismatch':
  header(d,'A definition is not proof.','Check against Delivery Operations’ all-due rule')
  panel(d,64,238,550,305,'Recorded rule: count all 4','50.0%','Includes the unfinished parcel')
  panel(d,640,238,576,305,'Query: count only 3','66.7%','Removes the unfinished parcel')
  text(d,'A successful query can answer the wrong question.',64,603,32,bold=True,color=RUST);add(im)
 elif k=='verify':
  header(d,'Check the calculation against the rule.')
  for j,(a,b) in enumerate([('Inspect the filter','Does it remove unfinished deliveries?'),('Inspect the denominator','Does it include all four deliveries due?'),('Compare with the example','Two on time out of four must give 50.0%.')]):
   im2,d2=layer();y=237+j*120;d2.ellipse((64,y,113,y+49),fill=WASH);text(d2,str(j+1),79,y+7,25,bold=True,color=RUST);text(d2,a,142,y-3,32,bold=True);text(d2,b,142,y+43,27,color=MUTED)
   add(im2,cue(t,['Inspect the filter','Inspect the denominator','Compare the calculation'][j]))
  text(d,'Rule changes? Review the definition and calculation.',64,632,27,color=GREEN);add(im)
 elif k=='recap':
  header(d,'Three questions to take to your next report.')
  for j,s in enumerate(['What counts?','When was it measured?','Which team can explain its meaning?']):
   text(d,f'0{j+1}',64,244+j*95,27,color=RUST);text(d,s,145,236+j*95,39,serif=True)
  d.rounded_rectangle((64,562,1216,653),radius=14,fill=SAGE);text(d,'Then check that the calculation follows the rule.',88,587,32,bold=True,color=GREEN);add(im)
 elif k=='end':
  text(d,'METADATA SYSTEMS  /  CHAPTER 1',64,75,22,bold=True,color=RUST)
  text(d,'What the data\ncannot tell you',64,170,66,serif=True)
  text(d,C['book_url'],64,422,34,width=1150,color=RUST)
  text(d,C['attribution'],64,515,28,color=MUTED)
  text(d,'Invented delivery example · synthetic narration',64,570,24,color=MUTED);add(im)
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
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'clips.txt'),'-i',str(P/'narration.wav'),'-i',str(P/'captions.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart','-metadata','title='+C['title'],'-metadata','comment=Authored chapter adaptation. Synthetic voice: '+C['voice']+'. Source: '+C['source_url'],str(P/'chapter-01.mp4')],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'captions.srt'),str(P/'captions.vtt')],check=True)
 print('FINAL VIDEO READY',flush=True)
