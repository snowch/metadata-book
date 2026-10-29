"""Screen completed samples for missing/changed words; no listening approval."""
from pathlib import Path
import argparse,difflib,hashlib,json,re
from math import gcd
import soundfile as sf
from scipy.signal import resample_poly
from faster_whisper import WhisperModel

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--input-dir',type=Path,required=True)
parser.add_argument('--text-file',type=Path,default=root.parent/'spoken.txt')
args=parser.parse_args()
expected=args.text_file.read_text().strip()
pending=[]
for path in sorted(args.input_dir.glob('voice-*.wav')):
 metadata=path.with_suffix('.json')
 if not metadata.exists() or json.loads(metadata.read_text()).get('status')!='complete':continue
 digest=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
 assert json.loads(metadata.read_text())['sha256']==digest, path
 dest=path.with_suffix('.audit.json')
 if dest.exists():
  old=json.loads(dest.read_text())
  if old.get('audio_sha256')==digest and old.get('expected')==expected:continue
 pending.append((path,dest,digest))
if not pending:raise SystemExit('No unaudited samples')
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=1)
def words(s):return re.findall(r'[a-z0-9]+',s.lower())
for path,dest,digest in pending:
 samples,rate=sf.read(path,dtype='float32');g=gcd(rate,16000)
 samples=resample_poly(samples,16000//g,rate//g)
 segments,_=model.transcribe(samples,language='en',beam_size=5,vad_filter=False,condition_on_previous_text=False)
 segments=[{'start':s.start,'end':s.end,'text':s.text} for s in segments]
 actual=' '.join(s['text'].strip() for s in segments)
 a,b=words(expected),words(actual)
 differences=[{'kind':op,'expected':' '.join(a[i:j]),'heard':' '.join(b[k:l])} for op,i,j,k,l in difflib.SequenceMatcher(None,a,b).get_opcodes() if op!='equal']
 report={'file':path.name,'audio_sha256':digest,'method':'faster-whisper small.en CPU int8; 1 thread; beam 5; no prompt; no VAD; no previous-text conditioning','expected':expected,'transcript':actual,'differences':differences,'segments':segments,'pronunciation_verified':False,'note':'Recognition differences require listening; this does not verify naturalness or pronunciation.'}
 dest.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'file':path.name,'differences':differences,'transcript':actual}),flush=True)
