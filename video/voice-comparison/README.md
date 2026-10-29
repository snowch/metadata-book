# Chapter 2 voice audition

Three voices read the same paragraph: the published Edge Sonia narration,
Qwen3-TTS 1.7B VoiceDesign, and Chatterbox Nano. The player at
`assets/video/voice-comparison/index.html` hides names until requested. This is
one audition per model, not a randomized study or a model-quality benchmark.
The chapter videos retain their existing narration pending listening feedback.

## Method

- `canonical.txt` preserves the chapter wording. `spoken.txt` expands SQLite to
  “sequel lite” and lowercases TEXT/NULL, using the same spoken words for both
  open models. The baseline is Chapter 2's existing `audio-01.wav`.
- Each open model generates the whole paragraph in one call. Qwen uses a
  designed adult British female voice and a conversational delivery instruction.
  Chatterbox uses its checkpoint's packaged default voice conditionals; no
  external recording or cloned speaker is supplied.
- Both open models run locally on CPU. Separate Python environments avoid conflicting
  model dependencies. Model weights are downloaded from pinned official Hugging
  Face revisions and checked against their published SHA-256 values.
- `package.py` uses two-pass FFmpeg loudness normalization targeting -18 LUFS,
  -2 dBTP, LRA 11, then encodes 24 kHz mono MP3 at 128 kbps. It does not change
  tempo, pitch, or trim pauses. Baseline includes the existing scene padding;
  the new samples retain the complete waveforms returned by the models.
- `audit.py` uses faster-whisper small.en, CPU int8, beam 5, no prompt, no VAD,
  and no previous-text conditioning. It flags transcript differences for human
  listening. It cannot establish pronunciation or naturalness, and is not an
  approval gate for replacing narration.

The code and weights are Apache-2.0 for Qwen and MIT for Chatterbox. The source
revision, model revision, settings, and actual run times are retained with each
sample. Chatterbox's built-in PerTh watermark is preserved.

## Reproduce

Run from this directory. Both models require several gigabytes of downloads.
Use Python 3.12 and FFmpeg. Keep the two environments separate.

```bash
python -m venv /tmp/qwen-venv
/tmp/qwen-venv/bin/pip install torch==2.15.0+cpu torchaudio==2.11.1+cpu --index-url https://download.pytorch.org/whl/cpu
/tmp/qwen-venv/bin/pip install qwen-tts==0.1.1 faster-whisper
# qwen-tts installation can replace the CPU audio wheel; restore it explicitly.
/tmp/qwen-venv/bin/pip install --force-reinstall --no-deps torchaudio==2.11.1+cpu --index-url https://download.pytorch.org/whl/cpu
python qwen/download_model.py
/tmp/qwen-venv/bin/python qwen/generate.py

python -m venv /tmp/chatterbox-venv
/tmp/chatterbox-venv/bin/pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
git clone https://github.com/resemble-ai/chatterbox chatterbox/source
git -C chatterbox/source checkout 5de7a54aa4e5e2baadb0182dde554908b48b85c2
/tmp/chatterbox-venv/bin/pip install -e chatterbox/source
python chatterbox/download_model.py
/tmp/chatterbox-venv/bin/python chatterbox/synthesize.py
cp chatterbox/sample-nano.wav chatterbox/sample.wav

# Rebuild Chapter 2 first if its intermediate scene audio is unavailable.
cp ../../out/chapter-02/audio-01.wav baseline.wav
/tmp/qwen-venv/bin/python audit.py
python package.py
```

Installed package versions are in the per-model lockfiles. Those files record
this run, including local editable installation paths; the commands above
explain how to recreate those checkouts rather than install a stale local path.
Large checkpoints and intermediate WAVs are ignored by Git. The published MP3s,
transcripts, audit results and metadata are retained for review.

## Results from 29 October 2026

Both open-model runs used two Torch threads on the same five-core CPU host;
there was no GPU. These are measured trial times under shared load, not a
throughput benchmark.

| Sample | Voice | Audio | Generation time (excluding model loading) |
| --- | --- | --- | --- |
| A | Existing Edge Sonia, British English, rate -2% | 33.50 s | Reused published scene audio |
| B | Qwen3-TTS 1.7B VoiceDesign | 32.48 s | 316.52 s |
| C | Chatterbox Nano, built-in voice | 29.96 s | 93.89 s |

The ASR screen recovered the complete sequence through “sole key” in all three
samples. It transcribed “sequel lite” as “SQL light” throughout. The baseline
and Chatterbox transcripts use the digit 0 for “zero”. Chatterbox's opening
“column” was recognized as “COM”, which needs particular attention by ear.
These are recognition differences, not confirmed pronunciation faults.
No listening-based quality winner or NotebookLM equivalence is asserted.
