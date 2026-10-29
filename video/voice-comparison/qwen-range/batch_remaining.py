"""Generate remaining original designs as one official Qwen voice-design batch.
Run with /tmp/qwen-venv/bin/python; accepts --model-dir, --output-dir, --text-file.
No cloned references, trimming, time stretching, or text rewriting.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import traceback
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel
from generate import VOICES, MODEL, ROOT, SOURCE, REVISION

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-dir', type=Path, default=MODEL)
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    parser.add_argument('--text-file', type=Path, default=SOURCE)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = args.text_file.resolve()
    passage = source.read_text().strip()
    torch.set_num_threads(4)
    start = time.monotonic()
    print('Loading pinned model for official batch of voices02-04', flush=True)
    model = Qwen3TTSModel.from_pretrained(str(args.model_dir), device_map='cpu', dtype=torch.bfloat16, attn_implementation='sdpa')
    loaded = time.monotonic()
    metas = []
    for index, (name, style) in enumerate(VOICES[1:], 2):
        metas.append(dict(name=name, model='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign', revision=REVISION,
            license='Apache-2.0', device='cpu', dtype='bfloat16', attention='sdpa', threads=4,
            seed=42, seed_scope='Reset once before the shared batch of voices02-04; not reset per voice',
            batch_size=3, batch_index=index-2, style=style, max_new_tokens=1200, language='English',
            source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            spoken_text=passage, model_load_seconds=loaded-start, cloned_reference=False,
            post_processing='PCM16 WAV encoding only; no trimming or time stretching'))
    torch.manual_seed(42)
    print('START batch voices02-04', flush=True)
    generated_at = time.monotonic()
    try:
        wavs, rate = model.generate_voice_design(text=[passage]*3, language=['English']*3,
            instruct=[style for name, style in VOICES[1:]], max_new_tokens=1200)
        elapsed = time.monotonic() - generated_at
        if len(wavs) != 3:
            raise ValueError(f'Expected three waves, got {len(wavs)}')
        for index, (wave, meta) in enumerate(zip(wavs, metas), 2):
            meta['batch_generation_seconds'] = elapsed
            wave = np.asarray(wave)
            if wave.ndim != 1 or not wave.size or not np.isfinite(wave).all():
                raise ValueError(f'Invalid wave{index}: {wave.shape}')
            path = output / f'voice-{index:02d}.wav'
            sf.write(path, wave, rate, subtype='PCM_16')
            decoded, read_rate = sf.read(path)
            info = sf.info(path)
            if read_rate != rate or len(decoded) != len(wave) or not np.isfinite(decoded).all() or info.format != 'WAV':
                raise ValueError(f'WAV{index} validation failed')
            meta.update(status='complete', sample_rate=rate, frames=len(wave), seconds=len(wave)/rate,
                channels=info.channels, container=info.format, subtype=info.subtype,
                generated_peak=float(np.max(np.abs(wave))), finite=True,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size)
            (output/f'voice-{index:02d}.json').write_text(json.dumps(meta,indent=2)+'\n')
            print('RESULT '+json.dumps(meta),flush=True)
    except Exception as exc:
        failure=dict(status='failed',batch_generation_seconds=time.monotonic()-generated_at,
            error=repr(exc),traceback=traceback.format_exc())
        (output/'batch-failure.json').write_text(json.dumps(failure,indent=2)+'\n')
        print('FAILURE '+json.dumps(failure),flush=True)
        raise
    all_metas=[json.loads((output/f'voice-{index:02d}.json').read_text()) for index in range(1,5)]
    (output/'metadata.json').write_text(json.dumps(all_metas,indent=2)+'\n')

if __name__ == '__main__':
    main()
