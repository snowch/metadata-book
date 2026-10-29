"""Generate four original voice designs offline using the existing pinned model.

Use --voices 1 for the first sample, then batch_remaining.py for the other three.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import time
import traceback

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

ROOT = Path(__file__).resolve().parent
MODEL = ROOT.parent / 'qwen/model'
SOURCE = ROOT.parent / 'spoken.txt'
REVISION = '5ecdb67327fd37bb2e042aab12ff7391903235d3'
VOICES = [
    ('British male colleague', 'An adult male voice with a natural British English accent and a warm mid-low register. Speak conversationally as a thoughtful colleague explaining a table: moderate pace, natural pauses and gently varied emphasis. Avoid theatrical or promotional delivery.'),
    ('American female explainer', 'An adult female voice with a natural American English accent, relaxed clear midrange tone. Explain the table conversationally with easy clarity, moderate pace, natural pauses and subtle emphasis. Avoid theatrical or promotional delivery.'),
    ('American male narrator', 'An adult male voice with a natural American English accent and a friendly reflective midrange tone. Narrate thoughtfully, with moderate pace, natural pauses and gentle emphasis on the explanation. Avoid theatrical or promotional delivery.'),
    ('British female documentary', 'A mature adult female voice with a natural British English accent, a lower-pitched resonant register and grounded documentary tone. Speak with calm measured clarity, moderate pace, natural pauses and restrained emphasis. Avoid theatrical or promotional delivery.'),
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-dir', type=Path, default=MODEL)
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    parser.add_argument('--text-file', type=Path, default=SOURCE)
    parser.add_argument('--voices', type=int, nargs='+', choices=range(1,5), default=[1,2,3,4])
    args = parser.parse_args()
    output = args.output_dir.resolve()
    source = args.text_file.resolve()
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(4)
    passage = source.read_text().strip()
    started = time.monotonic()
    print('Loading pinned model once, CPU BF16 SDPA, four threads', flush=True)
    model = Qwen3TTSModel.from_pretrained(str(args.model_dir), device_map='cpu', dtype=torch.bfloat16, attn_implementation='sdpa')
    load_seconds = time.monotonic() - started
    results = []
    for index, (name, style) in enumerate(VOICES, 1):
        if index not in args.voices:
            continue
        stem = f'voice-{index:02d}'
        meta = dict(name=name, model='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign', revision=REVISION,
                    license='Apache-2.0', device='cpu', dtype='bfloat16', attention='sdpa', threads=4,
                    seed=42, style=style, max_new_tokens=1200, language='English',
                    source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    spoken_text=passage, model_load_seconds=load_seconds, cloned_reference=False,
                    post_processing='PCM16 WAV encoding only; no trimming or time stretching')
        voice_start = time.monotonic()
        print(f'START {stem}: {name}', flush=True)
        try:
            torch.manual_seed(42)
            wavs, rate = model.generate_voice_design(text=passage, language='English', instruct=style, max_new_tokens=1200)
            meta['generation_seconds'] = time.monotonic() - voice_start
            wave = np.asarray(wavs[0])
            if wave.ndim != 1 or not wave.size or not np.isfinite(wave).all():
                raise ValueError(f'Invalid generated wave: shape={wave.shape}, finite={bool(np.isfinite(wave).all())}')
            path = output / f'{stem}.wav'
            sf.write(path, wave, rate, subtype='PCM_16')
            decoded, decoded_rate = sf.read(path)
            info = sf.info(path)
            if decoded_rate != rate or len(decoded) != len(wave) or not np.isfinite(decoded).all() or info.format != 'WAV':
                raise ValueError('WAV roundtrip validation failed')
            meta.update(status='complete', sample_rate=rate, frames=len(wave), seconds=len(wave)/rate,
                        channels=info.channels, container=info.format, subtype=info.subtype,
                        generated_peak=float(np.max(np.abs(wave))), finite=True,
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size)
        except Exception as exc:
            meta.update(status='failed', generation_seconds=time.monotonic()-voice_start,
                        error=repr(exc), traceback=traceback.format_exc())
        (output / f'{stem}.json').write_text(json.dumps(meta, indent=2)+'\n')
        results.append(meta)
        (output / 'metadata.json').write_text(json.dumps(results, indent=2)+'\n')
        print('RESULT '+json.dumps(meta), flush=True)

if __name__ == '__main__':
    main()
