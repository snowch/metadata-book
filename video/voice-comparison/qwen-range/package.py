"""Build the five-voice listening page from completed, audited Qwen samples."""
from pathlib import Path
import argparse,hashlib,html,json,subprocess,shutil
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--input-dir',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,default=root.parents[2]/'assets/video/voice-comparison')
args=parser.parse_args();out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
original_mp3=root.parents[2]/'assets/video/voice-comparison/sample-B.mp3'
if (out/'sample-B.mp3').resolve()!=original_mp3.resolve():
 shutil.copyfile(original_mp3,out/'sample-B.mp3')
expected=(root.parent/'spoken.txt').read_text().strip()
original=json.loads((root.parent/'qwen/metadata.json').read_text())
original_audit=json.loads((root.parent/'qwen/sample.audit.json').read_text())
voices=[dict(id='Q1',title='Warm British female',description='The original Qwen sample.',file='sample-B.mp3',seconds=original['seconds'],style=original['style'],audit=original_audit,generation=original)]
titles=['Warm British male','Relaxed American female','Reflective American male','British female · deeper voice']
descriptions=['Conversational, with a mid-low register.','Clear midrange voice, with an easy delivery.','Friendly midrange voice, with thoughtful pacing.','Mature, resonant voice, with a documentary delivery.']
for i,(title,description) in enumerate(zip(titles,descriptions),1):
 src=args.input_dir/f'voice-{i:02d}.wav';meta=json.loads(src.with_suffix('.json').read_text());audit=json.loads(src.with_suffix('.audit.json').read_text())
 digest=hashlib.file_digest(src.open('rb'),'sha256').hexdigest()
 assert meta['status']=='complete' and meta['sha256']==digest and audit['audio_sha256']==digest
 assert meta['spoken_text']==expected and audit['expected']==expected
 filt='loudnorm=I=-18:TP=-2:LRA=11'
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af',filt+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 m=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
 f=filt+':measured_I='+m['input_i']+':measured_TP='+m['input_tp']+':measured_LRA='+m['input_lra']+':measured_thresh='+m['input_thresh']+':offset='+m['target_offset']+':linear=true'
 filename=f'qwen-{i+1:02d}.mp3';dest=out/filename
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-af',f,'-ar','24000','-ac','1','-codec:a','libmp3lame','-b:a','128k',str(dest)],check=True)
 voices.append(dict(id=f'Q{i+1}',title=title,description=description,file=filename,seconds=meta['seconds'],style=meta['style'],audit=audit,generation=meta,loudness_analysis=m,mp3_sha256=hashlib.file_digest(dest.open('rb'),'sha256').hexdigest()))
cards=[]
for v in voices:
 flags=v['audit']['differences']
 items=''.join('<li>'+html.escape(d['expected'] or '(nothing)')+' → '+html.escape(d['heard'] or '(not transcribed)')+'</li>' for d in flags)
 check=('<p>Speech recognition returned these differences. They may be spelling differences or speech errors; listen to check.</p><ul>'+items+'</ul>') if flags else '<p>No word differences were flagged by speech recognition. Pronunciation still needs a listening check.</p>'
 cards.append(f'''<section aria-labelledby="{v['id']}"><div class="card-head"><span class="badge">{v['id']}</span><span class="duration">{v['seconds']:.0f} seconds</span></div><h2 id="{v['id']}">{html.escape(v['title'])}</h2><p class="description">{html.escape(v['description'])}</p><audio controls preload="metadata" aria-label="{v['id']}: {html.escape(v['title'])}" src="{v['file']}"></audio><details><summary>Transcript check</summary>{check}</details><details><summary>Voice direction</summary><p>{html.escape(v['style'])}</p></details></section>''')
passage=html.escape((root.parent/'canonical.txt').read_text())
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Five Qwen voices · Metadata systems</title><style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f7f4ed;color:#29302a;font:17px/1.55 system-ui,sans-serif}main{max-width:1020px;margin:40px auto;padding:0 24px}h1{font:2.7rem/1.12 Georgia,serif;margin:.5em 0}h2{font:1.45rem/1.2 Georgia,serif;margin:14px 0 8px}.eyebrow{font-size:.78rem;letter-spacing:.1em;color:#9b432c}.intro{max-width:700px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:28px 0}section{min-width:0;border:1px solid #d9d5cb;background:#fffdf8;border-radius:12px;padding:22px}.card-head{display:flex;align-items:center;justify-content:space-between;gap:12px}.badge{background:#eee0d3;color:#91402b;font-weight:650;padding:4px 10px;border-radius:5px}.duration,.description{color:#62675f}.description{min-height:2.8em;margin:8px 0 18px}audio{width:100%;display:block}summary{cursor:pointer;color:#98432c;padding:10px 0;min-height:44px}details p,details li{font-size:.9rem}details ul{padding-left:20px}a{color:#98432c;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:2px solid #98432c;outline-offset:3px}blockquote{border-left:3px solid #98432c;padding-left:20px;margin:14px 0}footer{font-size:.85rem;color:#62675f;margin:24px 0 40px}@media(max-width:620px){main{margin:24px auto;padding:0 18px}.grid{grid-template-columns:1fr}h1{font-size:2.2rem}.description{min-height:0}}
</style></head><body><main><p class="eyebrow">METADATA SYSTEMS · VOICE AUDITION</p><h1>Five Qwen voices</h1><div class="intro"><p>The same Chapter 2 passage, with five voice directions and matched playback volume. Q1 is the original sample; Q2–Q5 are new.</p><p>Listen for a voice you would enjoy learning from: clear, natural, and easy to follow.</p></div><div class="grid">'''+''.join(cards)+'''</div><details><summary>Read the passage</summary><blockquote>'''+passage+'''</blockquote></details><p><a href="index.html">Compare Qwen with the current narrator and Chatterbox →</a></p><footer>All voices are synthetic. Descriptions show the requested voice directions; accent and delivery still need your listening judgement. These samples use Qwen3-TTS VoiceDesign without reference recordings. Transcript checks screen for errors; they do not verify pronunciation or naturalness.</footer></main><script>document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()})))</script></body></html>'''
(out/'qwen.html').write_text(page)
(out/'qwen-manifest.json').write_text(json.dumps(voices,indent=2)+'\n')
print('Packaged five Qwen voices')
