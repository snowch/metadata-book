"""Download the pinned official Base model; reuse only hash-identical local files."""
from pathlib import Path
import urllib.request,json,concurrent.futures,hashlib,os
MODEL='Qwen/Qwen3-TTS-12Hz-1.7B-Base'
REVISION='fd4b254389122332181a7c3db7f27e918eec64e3'
root=Path(os.environ.get('QWEN_BASE_MODEL','/workspace/scratch/qwen-base/model'))
root.mkdir(parents=True,exist_ok=True)
reference=Path('/workspace/scratch/voice-trial/qwen/model')
manifest=json.load(urllib.request.urlopen(f'https://huggingface.co/api/models/{MODEL}/tree/{REVISION}?recursive=true'))
(root.parent/'download-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def download(entry):
 if entry['type']!='file':return
 path=root/entry['path'];path.parent.mkdir(parents=True,exist_ok=True)
 other=reference/entry['path'];expected=entry.get('lfs',{}).get('oid')
 if not path.exists() and other.exists() and expected:
  with other.open('rb') as source:identical=hashlib.file_digest(source,'sha256').hexdigest()==expected
  if identical:os.link(other,path)
 if not path.exists():
  tmp=path.with_suffix(path.suffix+'.part')
  with urllib.request.urlopen(f'https://huggingface.co/{MODEL}/resolve/{REVISION}/{entry["path"]}') as source,tmp.open('wb') as dest:
   while data:=source.read(1048576):dest.write(data)
  tmp.rename(path)
 assert path.stat().st_size==entry['size'],path
 if expected:
  with path.open('rb') as source:assert hashlib.file_digest(source,'sha256').hexdigest()==expected,path
 print(path.name,'verified',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(download,manifest))
