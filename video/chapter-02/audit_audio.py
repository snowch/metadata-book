"""Transcribe rendered speech for review. ASR is not a listening review."""
import argparse
import json
import os
from pathlib import Path
import subprocess

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--build', type=Path, default=Path(os.environ.get(
    'EXPLAINER_OUT', str(ROOT.parents[1] / 'out' / 'chapter-02'))))
ap.add_argument('--scenes', help='Comma-separated zero-based scenes to recheck; otherwise the complete narration')
ap.add_argument('--model', default='base.en')
args = ap.parse_args()
build = args.build.resolve()
model = WhisperModel(args.model, device='cpu', compute_type='int8', cpu_threads=2)
# Natural recognition: no vocabulary hints or digit suppression.
suppress = [-1]
paths = ([build / f'audio-{int(i):02}.wav' for i in args.scenes.split(',')]
         if args.scenes else [build / 'narration.wav'])
reports = []
for path in paths:
    # Decode through FFmpeg; this also avoids PyAV metadata_errors incompatibility.
    decoded = subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
        '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'],
        capture_output=True, check=True)
    audio = np.frombuffer(decoded.stdout, dtype=np.float32)
    segments, _ = model.transcribe(
        audio, language='en', beam_size=5, suppress_tokens=suppress,
        condition_on_previous_text=False, word_timestamps=True, vad_filter=True,
        initial_prompt=None)
    result = []
    for segment in segments:
        item = {'start': segment.start, 'end': segment.end, 'text': segment.text,
                'words': [{'word': w.word, 'start': w.start, 'end': w.end,
                           'probability': w.probability} for w in (segment.words or [])]}
        result.append(item)
        print(f'{path.name} {segment.start:.1f}: {segment.text}', flush=True)
    reports.append({'file': path.name, 'segments': result})
name = 'speech-audit-scenes-' + args.scenes.replace(',', '-') + '.json' if args.scenes else 'speech-audit.json'
(build / name).write_text(json.dumps({
    'method': 'Automated recognition; human listening not established by this report',
    'model': args.model, 'reports': reports}, indent=2), encoding='utf-8')

