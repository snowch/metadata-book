# Five Qwen voice directions

The listening page is `assets/video/voice-comparison/qwen.html`.
Q1 reuses the original Qwen sample from the three-model audition. Q2–Q5 use the
same pinned Qwen3-TTS 1.7B VoiceDesign model and the same spoken Chapter 2 passage,
with four new voice instructions. There are no reference recordings or cloned
speakers. The labels describe the requested voices; they are not independent
verification of accent, perceived gender or delivery.

| Player label | Source | Requested voice |
| --- | --- | --- |
| Q1 | Previous `qwen/sample.wav` | Warm British female |
| Q2 | `voice-01.wav` | Warm British male, mid-low register |
| Q3 | `voice-02.wav` | Relaxed American female, midrange |
| Q4 | `voice-03.wav` | Friendly, reflective American male |
| Q5 | `voice-04.wav` | Mature British female, lower resonant register |

## Reproduce

Use the existing CPU environment and pinned model setup documented in the
parent directory. From this directory:

```bash
/tmp/qwen-venv/bin/python generate.py \
  --model-dir ../qwen/model \
  --text-file ../spoken.txt \
  --output-dir ../../../out/qwen-voice-range --voices 1
/tmp/qwen-venv/bin/python batch_remaining.py \
  --model-dir ../qwen/model \
  --text-file ../spoken.txt \
  --output-dir ../../../out/qwen-voice-range
/tmp/qwen-venv/bin/python audit.py --input-dir ../../../out/qwen-voice-range
python package.py --input-dir ../../../out/qwen-voice-range
```

Q2 is generated alone with seed 42. Q3–Q5 are generated in one supported
batch, with seed 42 reset once for that batch. Both scripts use BF16, SDPA,
four CPU threads, and a 1,200-token ceiling. Batch timing is recorded for the
whole call, not attributed separately to each sample. Model revision and full instructions are saved for each sample.
The package script requires an audit matching each WAV's SHA-256 before
encoding it. It applies the same two-pass -18 LUFS/-2 dBTP loudness target as
Q1 and emits 24 kHz mono, 128 kbps MP3s without changing pace or trimming pauses.

The audit uses faster-whisper small.en with one CPU thread, int8, beam 5,
no prompt, no VAD, and no previous-text conditioning. Recognition differences
remain visible in the player. Neither a transcript match nor successful
waveform decoding establishes pronunciation quality or naturalness.

Intermediate WAVs are ignored by Git; model metadata and audit reports are
retained with the source, and the encoded samples are in the published assets.

## Recorded run

Q2 took 367.96 seconds to generate 37.12 seconds of audio. The shared call for
Q3–Q5 took 474.01 seconds and produced 30.48, 35.20 and 36.00 seconds respectively.
These CPU timings exclude model loading and are not a throughput benchmark.
An unfinished sequential attempt at Q3 was interrupted before any audio was
saved, then the remaining three were generated in the supported batch call.
All four WAVs passed finite-sample, container roundtrip and FFmpeg decode checks.

The automated transcripts reached the final sentence in each sample. Flags
include SQLite spelling variants and sole/soul homophones. Q4's transcript also
has “the” where the input says “this”; this remains a listening check rather
than a confirmed speech error. Full reports are retained beside each sample's
metadata and the flags are shown in the player. No listening approval is claimed.
