from pathlib import Path
import time,json,os
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TOKENIZERS_PARALLELISM']='false'
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel
root=Path(__file__).resolve().parent
torch.set_num_threads(2)
torch.manual_seed(42)
style='A warm adult female narrator with a natural British English accent. Explain this clearly to a colleague: conversational, thoughtful, gently varied emphasis, natural pauses, moderate pace. Avoid a theatrical or promotional delivery.'
start=time.monotonic()
print('Loading model',flush=True)
model=Qwen3TTSModel.from_pretrained(str(root/'model'),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
loaded=time.monotonic()
print('Loaded; generating whole passage',flush=True)
wavs,sr=model.generate_voice_design(text=(root.parent/'spoken.txt').read_text().strip(),language='English',instruct=style,max_new_tokens=1200)
end=time.monotonic()
sf.write(root/'sample.wav',wavs[0],sr)
meta={'model':'Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign','revision':'5ecdb67327fd37bb2e042aab12ff7391903235d3','license':'Apache-2.0','device':'cpu','dtype':'bfloat16','threads':2,'seed':42,'style':style,'sample_rate':sr,'seconds':len(wavs[0])/sr,'load_seconds':loaded-start,'generation_seconds':end-loaded,'max_new_tokens':1200}
(root/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta),flush=True)
