"""Download the pinned official Qwen checkpoint and verify published LFS hashes."""
from pathlib import Path
import urllib.request,json,concurrent.futures,hashlib
MODEL='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign'
REVISION='5ecdb67327fd37bb2e042aab12ff7391903235d3'
root=Path(__file__).resolve().parent/'model';root.mkdir(exist_ok=True)
manifest=json.load(urllib.request.urlopen(f'https://huggingface.co/api/models/{MODEL}/tree/{REVISION}?recursive=true'))
(root.parent/'download-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def download(entry):
 if entry['type']!='file':return
 path=root/entry['path'];path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  tmp=path.with_suffix(path.suffix+'.part')
  with urllib.request.urlopen(f'https://huggingface.co/{MODEL}/resolve/{REVISION}/{entry["path"]}') as source,tmp.open('wb') as dest:
   while data:=source.read(1048576):dest.write(data)
  tmp.rename(path)
 assert path.stat().st_size==entry['size'],path
 if entry.get('lfs'):
  with path.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==entry['lfs']['oid'],path
 print(path.name,'verified',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(download,manifest))
