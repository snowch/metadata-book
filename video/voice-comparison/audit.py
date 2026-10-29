from pathlib import Path
import json,re,difflib,time
import soundfile as sf
from scipy.signal import resample_poly
import numpy as np
from math import gcd
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parent
m=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2)
def words(s):return re.findall(r'[a-z0-9]+',s.lower())
expected=(root/'spoken.txt').read_text().strip()
for name,path in [('baseline',root/'baseline.wav'),('qwen',root/'qwen/sample.wav'),('chatterbox',root/'chatterbox/sample.wav')]:
 if not path.exists():continue
 dest=path.with_suffix('.audit.json')
 if dest.exists():continue
 samples,sr=sf.read(path,dtype='float32')
 g=gcd(sr,16000); samples=resample_poly(samples,16000//g,sr//g)
 segments,info=m.transcribe(samples,language='en',beam_size=5,vad_filter=False,condition_on_previous_text=False)
 ss=[{'start':s.start,'end':s.end,'text':s.text} for s in segments]
 actual=' '.join(s['text'].strip() for s in ss)
 a,b=words(expected),words(actual)
 diff=[{'kind':op,'expected':' '.join(a[i:j]),'heard':' '.join(b[k:l])} for op,i,j,k,l in difflib.SequenceMatcher(None,a,b).get_opcodes() if op!='equal']
 data={'name':name,'method':'faster-whisper small.en CPU int8; no prompt; beam 5','expected':expected,'transcript':actual,'differences':diff,'segments':ss,'pronunciation_verified':False,'note':'ASR is an error screen, not a listening review. Check every flagged span by ear.'}
 dest.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data),flush=True)
