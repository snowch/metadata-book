"""Q1 synthetic-reference cloning, unprompted ASR, and fresh canonical alignment.

Runs all chapters in a single model session. Raw audio and ASR are cached by
content and model provenance. ASR alignment is an estimate, not forced alignment
or evidence that unmatched canonical words were actually spoken.
"""
from pathlib import Path
import argparse,bisect,difflib,hashlib,json,math,os,re,subprocess,time,wave
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
from importlib.metadata import version
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
MODEL='Qwen/Qwen3-TTS-12Hz-1.7B-Base';REVISION='fd4b254389122332181a7c3db7f27e918eec64e3'
REFERENCE=Path(os.environ.get('Q1_REFERENCE',str(ROOT/'video'/'qwen-production'/'reference'/'q1.wav')))
REFERENCE_TEXT=Path(os.environ.get('Q1_REFERENCE_TEXT',str(ROOT/'video'/'qwen-production'/'reference'/'spoken.txt')))
SR=24000

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def spoken(text,config):
 lexicon=config.get('pronunciation',{})
 if lexicon:
  p=r'(?<!\w)(?:'+'|'.join(re.escape(k) for k in sorted(lexicon,key=len,reverse=True))+r')(?!\w)'
  text=re.sub(p,lambda m:lexicon[m[0]],text)
 return text.replace('—',', ').replace('“','"').replace('”','"').replace('’',"'")
def norm(text):return ''.join(c.lower() for c in text if c.isalnum())
def write(path,a):
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(a.astype(np.int16).tobytes())
def read(path):
 with wave.open(str(path),'rb') as w:
  assert w.getframerate()==SR and w.getnchannels()==1 and w.getsampwidth()==2
  return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).copy()
def stamp(t):
 n=round(t*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,ms=divmod(n,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
def save(path,value):
 temporary=path.with_name(path.name+f'.{os.getpid()}.tmp')
 temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)

def synthesize(jobs,args):
 import torch,soundfile as sf
 from qwen_tts import Qwen3TTSModel
 torch.set_num_threads(args.threads)
 model=Qwen3TTSModel.from_pretrained(args.model_dir,device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
 prompt=model.create_voice_clone_prompt(ref_audio=str(REFERENCE),ref_text=REFERENCE_TEXT.read_text().strip(),x_vector_only_mode=False)
 print('Q1 reusable synthetic-reference prompt ready',flush=True)
 for offset in range(0,len(jobs),args.batch_size):
  batch=jobs[offset:offset+args.batch_size];seed=42+offset
  torch.manual_seed(seed);start=time.monotonic()
  wavs,sr=model.generate_voice_clone(text=[j['spoken'] for j in batch],language=['English']*len(batch),voice_clone_prompt=prompt,max_new_tokens=1600)
  elapsed=time.monotonic()-start
  assert sr==SR and len(wavs)==len(batch)
  for audio in wavs:
   assert audio.ndim==1 and len(audio)>0 and np.isfinite(audio).all(), 'Invalid generated waveform'
   assert len(audio)/sr<130, 'Generation may have reached token limit; inspect before retrying'
   assert np.max(np.abs(audio))<1, 'Generated waveform would clip PCM16; inspect before retrying'
  members=[dict(spoken_sha256=hashlib.sha256(j['spoken'].encode()).hexdigest(),path=str(j['path'])) for j in batch]
  for job,audio in zip(batch,wavs):
   sf.write(job['path'],audio,sr,subtype='PCM_16')
   save(job['meta'],dict(job['provenance'],signature=job['signature'],seed=seed,batch_size=len(batch),batch_members=members,sdk_versions={name:version(name) for name in ('qwen-tts','torch','torchaudio','transformers','numpy','soundfile')},generation_batch_seconds=elapsed,seconds=len(audio)/sr,sha256=sha(job['path'])))
  print(json.dumps({'batch':[str(j['path']) for j in batch],'seconds':round(elapsed,2),'audio_seconds':[round(len(a)/sr,2) for a in wavs]}),flush=True)

def transcribe(jobs,args):
 from faster_whisper import WhisperModel
 model=WhisperModel(args.asr_model,device='cpu',compute_type='int8',cpu_threads=getattr(args,'asr_threads',2))
 for job in jobs:
  dest=job['path'].with_name('asr-'+job['path'].stem.split('-')[-1]+'.json');signature=sha(job['path'])
  if dest.exists():
   cached=json.loads(dest.read_text())
   if cached.get('audio_sha256')==signature and cached.get('model')==args.asr_model and cached.get('expected')==job['spoken']:continue
  decoded=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(job['path']),'-ar','16000','-ac','1','-f','f32le','-'])
  start=time.monotonic()
  segments,_=model.transcribe(np.frombuffer(decoded,dtype=np.float32),language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False,initial_prompt=None,suppress_tokens=[-1],vad_filter=True)
  segments=list(segments);words=[dict(text=w.word,start=w.start,end=w.end,probability=w.probability) for s in segments for w in (s.words or [])]
  text=' '.join(s.text.strip() for s in segments)
  save(dest,dict(audio_sha256=signature,model=args.asr_model,vocabulary_prompt=None,digit_suppression=False,text=text,words=words,expected=job['spoken'],method='Independent unprompted ASR; not a listening review',seconds=time.monotonic()-start))
  print(str(dest),text,flush=True)

def expanded_asr(text,config,expected_text=""):
 from num2words import num2words
 text=spoken(text,config)
 # Reconcile clock formatting only where that literal time occurs in this scene.
 clocks={'twelve twenty':('1220','12.20','12:20','.20'),
         'twelve thirty':('1230','12.30','12:30','.30')}
 for phrase,variants in clocks.items():
  if re.search(r'\b'+re.escape(phrase)+r'\b',expected_text,re.IGNORECASE):
   for variant in variants:
    value=phrase.split(' ',1)[1] if variant.startswith('.') else phrase
    text=re.sub(r'(?<!\d)'+re.escape(variant)+r'(?![\d%])',value,text)
 # Whisper can split decimal spellings and identifier letters into separate words.
 identifier_numbers={}
 for key,value in config.get('pronunciation',{}).items():
  identifier=re.fullmatch(r'([A-Za-z])(\d+)',key)
  if identifier and value.lower().startswith(identifier[1].lower()+' '):identifier_numbers[identifier[2]]=value[2:]
 # Known 1205 identifiers and clock times are commonly recognised as 12.05.
 # Preserve the original ASR elsewhere; this only reconciles its numeric spelling.
 for digits,value in identifier_numbers.items():
  if len(digits)==4 and ' oh ' in value:
   hour=str(int(digits[:2]));minute=digits[2:]
   text=re.sub(r'(?<!\d)'+hour+r'[.:]'+minute+r'(?![\d%])',value,text)
   text=re.sub(r'(?<!\d)[.:]'+minute+r'(?![\d%])','oh '+value.split(' oh ',1)[1],text)
 text=re.sub(r'(?<!\d)\.(?=\d)',' point ',text)
 def number(match):
  value=match[0]
  if value in identifier_numbers:return identifier_numbers[value]
  if '.' in value:
   whole,fraction=value.split('.')
   return num2words(int(whole))+' point '+' '.join(num2words(int(c)) for c in fraction)
  return num2words(int(value))
 return re.sub(r'\d+(?:\.\d+)?',number,text).replace('%',' percent')

def align(text,asr,duration,config):
 """Transfer real ASR character times to canonical words; interpolate gaps."""
 canonical=text.split();wanted=''.join(norm(w) for w in canonical)
 recognised='';times=[]
 for word in asr['words']:
  value=norm(expanded_asr(word['text'],config,text));recognised+=value
  for i in range(len(value)):times.append(word['start']+(word['end']-word['start'])*(i+.5)/len(value))
 matcher=difflib.SequenceMatcher(None,wanted,recognised,autojunk=False)
 anchors={}
 for block in matcher.get_matching_blocks():
  for i in range(block.size):anchors[block.a+i]=times[block.b+i]
 if not anchors:raise ValueError('ASR produced no matching speech')
 positions=sorted(anchors);values=[anchors[i] for i in positions]
 estimated=np.interp(np.arange(len(wanted)),positions,values)
 boundaries=np.concatenate([[max(0,float(estimated[0])-.04)],(estimated[:-1]+estimated[1:])/2,[min(duration,float(estimated[-1])+.06)]])
 words=[];pos=0
 for value in canonical:
  n=len(norm(value))
  if not n:continue
  start=float(boundaries[pos]);end=float(boundaries[pos+n])
  if end<=start:end=start # Omitted/unmatched words may have no timing extent; flagged in alignment.
  words.append(dict(text=value,offset=round(start*1e7),duration=round((end-start)*1e7),matched_characters=sum(i in anchors for i in range(pos,pos+n)),characters=n))
  pos+=n
 differences=[dict(operation=tag,expected=wanted[a:b],recognised=recognised[c:d]) for tag,a,b,c,d in matcher.get_opcodes() if tag!='equal']
 return words,dict(matched_character_fraction=len(anchors)/len(wanted),differences=differences,warning='Canonical words with incomplete ASR matches use interpolated timing; inspect the independent ASR transcript for fidelity.')

def assemble(chapter,build,args):
 config=json.loads((chapter/'project.json').read_text());scenes=json.loads((chapter/'narration.json').read_text())
 all_audio=[];timings=[];captions=[];screening=[];cursor=0
 for i,scene in enumerate(scenes):
  if not scene['text']:
   audio=np.zeros(SR*5,dtype=np.int16);timings.append(dict(scene,number=i,start=cursor,duration=5,cues=[]));all_audio.append(audio);cursor+=5;continue
  raw=build/f'raw-{i:02}.wav';audio=read(raw);asr=json.loads((build/f'asr-{i:02}.json').read_text())
  words,alignment=align(spoken(scene['text'],config),asr,len(audio)/SR,config)
  screening.append(dict(scene=i,kind=scene['kind'],expected=spoken(scene['text'],config),recognised=asr['text'],audio_sha256=sha(raw),asr_file=f'asr-{i:02}.json',alignment=alignment))
  # Preserve all generated content. No first/last-word trim can hide omissions.
  lead=.25;tail=4.5 if scene['kind']=='pause' else .7 if scene['kind']=='title' else .45
  hold=scene.get('hold_seconds',0)
  if isinstance(hold,bool) or not isinstance(hold,(int,float)) or not math.isfinite(hold) or not 0<=hold<=15:
   raise ValueError('hold_seconds must be a finite number between zero and fifteen')
  tail+=hold
  shift=lead
  save(build/f'words-{i:02}.json',dict(signature=sha(raw),words=words,audio_time_offset_seconds=shift,timing_source='ASR alignment to canonical spoken text',asr_source=f'asr-{i:02}.json',alignment=alignment))
  audio=np.concatenate([np.zeros(round(lead*SR),dtype=np.int16),audio,np.zeros(round(tail*SR),dtype=np.int16)])
  duration=math.ceil(len(audio)/SR*24)/24;audio=np.pad(audio,(0,round(duration*SR)-len(audio)))
  ends=[];joined=''
  for word in words:joined+=norm(word['text']);ends.append(len(joined))
  assert joined==norm(spoken(scene['text'],config))
  cues=[];charpos=0
  for sentence in re.findall(r'.+?(?:[.!?][”"]?(?=\s|$)|$)',scene['text']):
   sentence=sentence.strip()
   if not sentence:continue
   n=len(norm(spoken(sentence,config)));first=bisect.bisect_right(ends,charpos);last=bisect.bisect_left(ends,charpos+n)
   start=words[first]['offset']/1e7+shift;finish=(words[last]['offset']+words[last]['duration'])/1e7+shift
   cues.append(dict(start=start,end=finish,text=sentence))
   chunks=[];chunk=[]
   for word in sentence.split():
    if len(' '.join(chunk+[word]))>86 and chunk:chunks.append(' '.join(chunk));chunk=[]
    chunk.append(word)
   if chunk:chunks.append(' '.join(chunk))
   if len(chunks)>1 and (len(chunks[-1])<24 or len(chunks[-1].split())<3):
    pair=(chunks[-2]+' '+chunks[-1]).split();splits=[k for k in range(1,len(pair)) if max(len(' '.join(pair[:k])),len(' '.join(pair[k:])))<=86]
    k=min(splits,key=lambda k:abs(len(' '.join(pair[:k]))-len(' '.join(pair[k:]))));chunks[-2:]=[' '.join(pair[:k]),' '.join(pair[k:])]
   for chunk in chunks:
    n=len(norm(spoken(chunk,config)));first=bisect.bisect_right(ends,charpos);last=bisect.bisect_left(ends,charpos+n)
    ca=words[first]['offset']/1e7+shift;cb=(words[last]['offset']+words[last]['duration'])/1e7+shift
    captions.append((cursor+ca,cursor+cb,chunk));charpos+=n
  assert charpos==len(joined)
  write(build/f'audio-{i:02}.wav',audio);all_audio.append(audio);timings.append(dict(scene,number=i,start=cursor,duration=duration,cues=cues));cursor+=duration
 write(build/'narration.wav',np.concatenate(all_audio));save(build/'timings.json',timings)
 save(build/'speech-audit.json',dict(method='Independent unprompted full-scene ASR screening; no human listening review',model=args.asr_model,vocabulary_prompt=None,digit_suppression=False,scenes=screening))
 (build/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{text}' for i,(a,b,text) in enumerate(captions))+'\n')
 (build/'transcript.txt').write_text(config['title']+'\n\nDisplay narration, preserved in full.\nSynthetic voice: '+config['voice']+'.\nSource: '+config['source_url']+'\n\n'+'\n\n'.join(s['text'] for s in scenes if s['text']))
 print(chapter.name,'TOTAL DURATION',cursor,flush=True)
 assert config['min_seconds']<=cursor<=config['max_seconds'], f'Chapter duration {cursor:.2f}s lies outside the project contract; review pacing before rendering'

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--chapters',default='01,02,03');ap.add_argument('--batch-size',type=int,default=6);ap.add_argument('--threads',type=int,default=4);ap.add_argument('--model-dir',default='/workspace/scratch/qwen-base/model');ap.add_argument('--asr-model',default='small.en');ap.add_argument('--validate',action='store_true');ap.add_argument('--assemble-only',action='store_true');ap.add_argument('--generate-only',action='store_true');ap.add_argument('--asr-threads',type=int,default=2);args=ap.parse_args()
 reference_provenance=json.loads((ROOT/'video'/'qwen-production'/'reference'/'q1.json').read_text())
 if sha(REFERENCE)!=reference_provenance['sha256'] or sha(REFERENCE_TEXT)!=reference_provenance['transcript_sha256']:
  raise ValueError('Q1 reference audio or transcript differs from the approved source provenance')
 if os.environ.get('EXPLAINER_OUT') and len(args.chapters.split(','))>1:
  raise ValueError('EXPLAINER_OUT requires a single --chapters value to avoid overwriting chapter files')
 chapters=[];jobs=[];pending=[]
 for number in args.chapters.split(','):
  chapter=ROOT/'video'/f'chapter-{number}';build=Path(os.environ.get('EXPLAINER_OUT',str(ROOT/'out'/f'q1-chapter-{number}'))).resolve();build.mkdir(parents=True,exist_ok=True);chapters.append((chapter,build))
  config=json.loads((chapter/'project.json').read_text());scenes=json.loads((chapter/'narration.json').read_text())
  for i,scene in enumerate(scenes):
   if not scene['text']:continue
   text=spoken(scene['text'],config)
   provenance=dict(model=MODEL,revision=REVISION,reference_audio_sha256=sha(REFERENCE),reference_text_sha256=sha(REFERENCE_TEXT),device='cpu',dtype='bfloat16',threads=args.threads,spoken_text=text,reference_origin='User-approved Q1 original synthetic VoiceDesign sample',max_new_tokens=1600)
   signature=hashlib.sha256(json.dumps(provenance,sort_keys=True).encode()).hexdigest()
   job=dict(path=build/f'raw-{i:02}.wav',meta=build/f'raw-{i:02}.metadata.json',spoken=text,provenance=provenance,signature=signature);jobs.append(job)
   if norm(text)==norm(REFERENCE_TEXT.read_text()):
    import shutil
    if not job['path'].exists() or sha(job['path'])!=sha(REFERENCE):shutil.copyfile(REFERENCE,job['path'])
    save(job['meta'],dict(provenance,signature=signature,reused_approved_reference=True,generation_method='reused approved reference',original_generation=dict(model='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign',revision='5ecdb67327fd37bb2e042aab12ff7391903235d3',seed=42),sha256=sha(job['path'])));continue
   if not job['path'].exists() or not job['meta'].exists() or json.loads(job['meta'].read_text()).get('signature')!=signature or json.loads(job['meta'].read_text()).get('sha256')!=sha(job['path']):pending.append(job)
 if args.validate:
  build=ROOT/'out'/'q1-validation';build.mkdir(parents=True,exist_ok=True)
  text='Metadata is information that describes data: its structure, meaning, origin and use. Two on time out of three completed gives sixty six point seven percent.'
  job=dict(path=build/'raw-00.wav',meta=build/'raw-00.metadata.json',spoken=text,provenance=dict(jobs[0]['provenance'],spoken_text=text),signature='q1-clone-validation-v1');pending=[job];jobs=[job]
 pending.sort(key=lambda job:len(job['spoken'].split()),reverse=True)
 if pending and not args.assemble_only:synthesize(pending,args)
 if args.generate_only:
  print('All generation complete; ASR and assembly deferred by --generate-only',flush=True);return
 if not args.assemble_only:transcribe(jobs,args)
 if not args.validate:
  for chapter,build in chapters:assemble(chapter,build,args)
if __name__=='__main__':main()
