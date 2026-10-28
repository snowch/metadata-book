"""Chapter-specific visuals, using the authored narration workflow's scene/mux pattern."""
from pathlib import Path
import hashlib,json,math,os,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('EXPLAINER_OUT',str(ROOT.parents[1]/'out'/'chapter-02'))).resolve()
C=json.loads((ROOT/'project.json').read_text());T=json.loads((P/'timings.json').read_text())
W,H=1280,720;BG='#f7f4ed';INK='#292d29';MUTED='#68685f';RUST='#96432e';WASH='#eee1d4';GREEN='#386854';SAGE='#e3eee6';LINE='#ddd8cd';SURFACE='#fffdf8'
FD=Path(C['font_dir']);FONTS=[FD/'DejaVuSans.ttf',FD/'DejaVuSans-Bold.ttf',FD/'DejaVuSerif.ttf',FD/'DejaVuSansMono.ttf']
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
 text(d,'METADATA SYSTEMS  /  CHAPTER 2',64,30,18,bold=True,color=RUST)
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


# Every SQL line is copied from examples/deliveries.sql; no ellipses.
VIEW_SQL = """CREATE VIEW on_time_completed AS
SELECT
    COUNT(*) AS completed,
    SUM(CASE WHEN delivered_at <= promised_at THEN 1 ELSE 0 END) AS on_time,
    ROUND(
        100.0 * SUM(CASE WHEN delivered_at <= promised_at THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS percentage
FROM deliveries
WHERE delivered_at IS NOT NULL;"""

def card(d,x,y,w,h,title,body,color=RUST):
 d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=SURFACE,outline=LINE,width=2)
 text(d,title,x+24,y+22,33,width=w-48,serif=True,color=color)
 text(d,body,x+24,y+84,29,width=w-48)

def sql(d,body,x,y,size=24,line_height=34,color=INK):
 f=ImageFont.truetype(str(FONTS[3]),size)
 for j,line in enumerate(body.splitlines()):
  if d.textlength(line,font=f)>W-64-x or y+j*line_height+size>H-32:raise ValueError('SQL overflow: '+line)
  d.text((x,y+j*line_height),line,font=f,fill=color)

def data_table(d,y=229):
 starts=[78,348,638,929]
 for x,label in zip(starts,['Delivery','Promised by','Delivered at','Status']):text(d,label,x,y,27,bold=True,color=MUTED)
 rows=[('D101','12:00','11:50','On time'),('D102','12:00','12:20','Late'),('D103','12:00','11:40','On time'),('D104','12:00','NULL','Unfinished')]
 for j,row in enumerate(rows):
  yy=y+47+j*54;d.rounded_rectangle((64,yy,1216,yy+49),radius=6,fill=SURFACE if j!=3 else WASH)
  for x,word in zip(starts,row):text(d,word,x,yy+6,28,width=265,color=GREEN if row[-1]=='On time' else INK)

def make(t):
 k=t['kind'];layers=[]
 def add(im,start=0,end=None):layers.append((im,start,end))
 im,d=layer()
 if k=='opening':
  header(d,'What a database already knows','Four invented deliveries · one table named deliveries')
  for j,(a,b) in enumerate([('Names','Which columns exist?'),('Declared types','What type is declared?'),('Constraints','Which values are allowed?')]):
   card(d,64+j*392,261,368,265,a,b)
  text(d,'Database records describe structure. What do the values mean?',64,591,31,bold=True,color=GREEN);add(im)
 elif k=='columns':
  header(d,'Inspect the column records.','SQLite · actual result for the deliveries table')
  sql(d,'SELECT name, type, "notnull", pk\nFROM pragma_table_xinfo(\'deliveries\') ORDER BY cid;',64,220,25,35)
  starts=[81,496,722,1012];widths=[395,206,270,180]
  for x,label in zip(starts,['name','type','notnull','pk']):text(d,label,x,321,29,bold=True,color=MUTED)
  for j,row in enumerate([('delivery_id','TEXT','1','1'),('promised_at','TEXT','1','0'),('delivered_at','TEXT','0','0')]):
   y=372+j*57;d.rounded_rectangle((64,y,1216,y+51),radius=6,fill=SURFACE)
   for x,w,v in zip(starts,widths,row):text(d,v,x,y+7,29,width=w,bold=v in ('1','0'))
  text(d,'notnull: 1 requires a value; 0 allows NULL.',64,559,29,bold=True,color=GREEN)
  text(d,'pk: position in the primary key; 0 means outside the key.',64,602,28)
  text(d,'TEXT is a declared type, not a strict guarantee here.',64,644,28,color=MUTED);add(im)
 elif k=='meaning':
  header(d,'Structure does not settle meaning.','A missing delivered_at value is permitted. What does it mean?')
  for j,(a,b) in enumerate([('Unfinished','Parcel has not arrived'),('Late update','Record has not caught up'),('Unknown time','Arrival time unavailable')]):card(d,64+j*392,240,368,265,a,b)
  d.rounded_rectangle((64,548,1216,654),radius=14,fill=SAGE)
  text(d,'For these complete invented records: NULL means not yet delivered.',88,574,30,width=1104,bold=True,color=GREEN);add(im)
 elif k=='promise':
  header(d,'Which promise does the column store?','One arrival, two interpretations')
  arrow(d,130,360,1150,360)
  for x,time,label in [(190,'12:00','Original promise'),(790,'12:20','Parcel arrives'),(1090,'12:30','Revised promise')]:
   d.line((x,345,x,375),fill=RUST if x==190 else GREEN,width=4)
   text(d,time,x-58,294,33,width=150,bold=True)
   text(d,label,x-112,396,28,width=225,color=MUTED)
  card(d,64,501,555,146,'Against noon: late','Same column name and type',RUST)
  card(d,645,501,571,146,'Against 12:30: on time','Meaning changes the measure',GREEN);add(im)
 elif k=='view':
  header(d,'Read the complete saved query.','A view recalculates from deliveries whenever it is read.')
  d.rounded_rectangle((64,219,1216,630),radius=13,fill=SURFACE,outline=LINE,width=2)
  sql(d,VIEW_SQL,82,237,24,34)
  text(d,'No completed rows? NULLIF guards the zero denominator.',64,650,27,color=MUTED);add(im)
  im,d=layer();d.rounded_rectangle((73,572,1206,615),radius=6,outline=RUST,width=3);add(im,cue(t,'Its filter removes'))
 elif k=='count':
  header(d,'The denominator changes the question.','Invented snapshot · 19 October 2026, 13:00 UTC · all four due by noon')
  data_table(d)
  for x,title,result,note in [(64,'Completed deliveries','2 / 3 = 66.7%','View excludes the unfinished parcel'),(652,'All deliveries due','2 / 4 = 50.0%','Delivery Operations definition')]:
   d.rounded_rectangle((x,519,x+564,678),radius=13,fill=SURFACE,outline=LINE,width=2)
   text(d,title,x+22,530,28,bold=True,color=MUTED)
   text(d,result,x+22,569,45,serif=True,color=RUST if x==64 else GREEN)
   text(d,note,x+22,636,28,width=520)
  add(im)
 elif k=='assumptions':
  header(d,'Check the storage assumption and the evidence.')
  d.rounded_rectangle((64,228,1216,362),radius=13,fill=WASH)
  sql(d,'YYYY-MM-DD HH:MM    →    2026-10-19 12:00',88,247,27,35)
  text(d,'Same fixed UTC format: text order matches time order.',88,302,29)
  card(d,64,408,522,192,'Saved query = metadata','Describes the calculation')
  card(d,694,408,522,192,'66.7% = output data','Returned when the view is read',GREEN)
  arrow(d,600,500,680,500)
  text(d,'The TEXT declaration does not enforce this timestamp format.',64,637,29,color=MUTED);add(im)
 elif k=='catalogues':
  header(d,'Two main jobs for a catalogue','The roles overlap; their main purpose differs.')
  card(d,64,232,558,315,'Help software read data','Database / query-engine catalogue\nHive Metastore\nSchemas · partitions\nStorage locations · file formats')
  card(d,650,232,566,315,'Help people understand data','Discovery / governance catalogue\nDataHub · OpenMetadata\nDefinitions · responsible teams\nLineage',GREEN)
  d.rounded_rectangle((64,584,1216,672),radius=13,fill=SAGE)
  text(d,'Overlap: database catalogues can hold comments and ownership.',88,608,29,width=1104,bold=True,color=GREEN);add(im)
 elif k=='recap':
  header(d,'Read the structure. Check the meaning.','Then inspect what the calculation actually counts.')
  for j,(a,b) in enumerate([('Structure','Which values are allowed?'),('Meaning','Which promise? What does NULL mean?'),('Calculation','Which deliveries enter the denominator?')]):card(d,64+j*392,249,368,307,a,b)
  text(d,'Useful evidence + an explicit definition = a measure you can explain.',64,611,30,bold=True,color=GREEN);add(im)
 elif k=='end':
  text(d,'METADATA SYSTEMS  /  CHAPTER 2',64,75,22,bold=True,color=RUST)
  text(d,'What a database\nalready knows',64,170,65,serif=True)
  text(d,C['book_url'],64,422,34,width=1150,color=RUST)
  text(d,C['attribution'],64,515,28,color=MUTED)
  text(d,'Invented example · synthetic narration',64,570,27,color=MUTED);add(im)
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
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'clips.txt'),'-i',str(P/'narration.wav'),'-i',str(P/'captions.srt'),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart','-metadata','title='+C['title'],'-metadata','comment=Authored chapter adaptation. Synthetic voice: '+C['voice']+'. Source: '+C['source_url'],str(P/'chapter-02.mp4')],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'captions.srt'),str(P/'captions.vtt')],check=True)
 print('FINAL VIDEO READY',flush=True)
