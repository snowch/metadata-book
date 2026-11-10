"""Independent ASR anchors aligned to canonical text; timestamps are estimates."""
from pathlib import Path
import importlib.util,json,re,subprocess
import numpy as np
from faster_whisper import WhisperModel
ROOT=Path(__file__).resolve().parents[2];build=ROOT/'out/chapter-01-v2'
spec=importlib.util.spec_from_file_location('alignment',ROOT/'video/qwen-production/synthesize.py');alignment=importlib.util.module_from_spec(spec);spec.loader.exec_module(alignment)
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
scenes=json.loads((build/'scenes.json').read_text());timeline=json.loads((build/'timeline.json').read_text());starts={s['id']:s['t']-timeline['start'] for s in timeline['scenes']};captions=[]
for scene in scenes:
 sid=scene['id'];raw=build/'audio'/f'{sid}.wav';dest=build/'audio'/f'{sid}.asr.json'
 if dest.exists():asr=json.loads(dest.read_text())
 else:
  data=subprocess.check_output(['ffmpeg','-v','error','-i',str(raw),'-ar','16000','-ac','1','-f','f32le','-'])
  segments,_=model.transcribe(np.frombuffer(data,dtype=np.float32),language='en',word_timestamps=True,condition_on_previous_text=False,initial_prompt=None)
  segments=list(segments);asr=dict(text=' '.join(s.text.strip() for s in segments),words=[dict(text=w.word,start=w.start,end=w.end,probability=w.probability) for s in segments for w in s.words]);dest.write_text(json.dumps(asr,indent=2)+'\n')
 import soundfile as sf
 words,report=alignment.align(scene['text'],asr,sf.info(raw).duration,{'pronunciation':{}})
 (build/'audio'/f'{sid}.alignment.json').write_text(json.dumps(report,indent=2)+'\n')
 for i in range(0,len(words),8):
  chunk=words[i:i+8];start=starts[sid]+chunk[0]['offset']/1e7;end=starts[sid]+(chunk[-1]['offset']+chunk[-1]['duration'])/1e7
  captions.append((start,end,' '.join(w['text'] for w in chunk)))
 print(sid,asr['text'],report['matched_character_fraction'],flush=True)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(build/'out/captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{t}' for i,(a,b,t) in enumerate(captions,1))+'\n')
