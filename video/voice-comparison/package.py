from pathlib import Path
import subprocess,json,html,base64,hashlib
root=Path(__file__).resolve().parent
out=root.parents[1]/'assets/video/voice-comparison';out.mkdir(parents=True,exist_ok=True)
voices=[('A','Current voice · Edge Sonia',root/'baseline.wav'),('B','Qwen3-TTS · designed British narrator',root/'qwen/sample.wav'),('C','Chatterbox Nano · built-in voice',root/'chatterbox/sample.wav')]
manifest=[];cards=[]
for letter,label,src in voices:
 if not src.exists():continue
 filt='loudnorm=I=-18:TP=-2:LRA=11'
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af',filt+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 m=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
 f=filt+':measured_I='+m['input_i']+':measured_TP='+m['input_tp']+':measured_LRA='+m['input_lra']+':measured_thresh='+m['input_thresh']+':offset='+m['target_offset']+':linear=true'
 dest=out/f'sample-{letter}.mp3'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-af',f,'-ar','24000','-ac','1','-codec:a','libmp3lame','-b:a','128k',str(dest)],check=True)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dest)]))
 manifest.append({'sample':letter,'voice':label,'duration_seconds':duration,'source':str(src.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'loudness_analysis':m})
 uri='data:audio/mpeg;base64,'+base64.b64encode(dest.read_bytes()).decode()
 auditpath=src.with_suffix('.audit.json')
 audit=json.loads(auditpath.read_text()) if auditpath.exists() else {}
 flags='; '.join(f"{d['expected']} → {d['heard']}" for d in audit.get('differences',[]))
 auditnote=('<details><summary>Transcript check</summary><p>Automatic recognition flagged: '+html.escape(flags)+'. These are listening checks, not confirmed speech errors.</p></details>') if flags else ''
 cards.append(f'<section><h2>Sample {letter}</h2><audio controls preload="metadata" aria-label="Sample {letter}" src="{uri}"></audio><details><summary>Reveal voice</summary><p>{html.escape(label)}</p></details>{auditnote}</section>')
canonical=(root/'canonical.txt').read_text()
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 2 · Voice comparison</title><style>
:root{color-scheme:light}body{background:#f7f4ed;color:#29302a;font:18px/1.6 system-ui,sans-serif;max-width:820px;margin:40px auto;padding:0 24px}h1{font:2.4rem/1.15 Georgia,serif}h2{font-size:1.1rem}section{border:1px solid #d9d5cb;background:#fffdf8;border-radius:12px;padding:18px 24px;margin:18px 0}audio{width:100%}summary{cursor:pointer;color:#9b432c;margin-top:12px}.label{font-size:.8rem;letter-spacing:.1em;color:#9b432c}blockquote{border-left:3px solid #9b432c;padding-left:20px;margin:24px 0}footer{font-size:.85rem;color:#666}a{color:#9b432c}</style><p class="label">METADATA SYSTEMS · LISTENING TRIAL</p><h1>Which voice is easiest to learn from?</h1><p>Three synthetic voices, one Chapter 2 passage. Listen before revealing the names. Volume is matched; each voice keeps its own pace.</p><p>Which sounds most natural, clear, and easy to follow? The transcript checks flag words to listen to carefully.</p>'''+''.join(cards)+'<details><summary>Read the passage</summary><blockquote>'+html.escape(canonical)+'</blockquote></details><footer><p>A first audition of one voice per model. Open-model samples were generated locally using a designed or built-in voice. Automated transcript checks do not verify pronunciation or naturalness.</p></footer><script>document.querySelectorAll("audio").forEach(a=>a.addEventListener("play",()=>document.querySelectorAll("audio").forEach(b=>{if(b!==a)b.pause()})))</script></html>'
# The hosted player uses separate audio files to keep the page small.
web=page
for letter,label,src in voices:
 mp3=out/f'sample-{letter}.mp3'
 if mp3.exists():web=web.replace('data:audio/mpeg;base64,'+base64.b64encode(mp3.read_bytes()).decode(),mp3.name)
(out/'index.html').write_text(web)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
