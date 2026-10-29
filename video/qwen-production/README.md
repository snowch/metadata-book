# Q1 chapter production

Q1 is the user-approved original synthetic warm British female voice created
with `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` at revision
`5ecdb67327fd37bb2e042aab12ff7391903235d3`. Its approved reference WAV SHA-256 is
`fcc306527e8923ad02fa751be3af11bd717add1b6160d19b0532014c722ee17a`.
The exact reference WAV and matching spoken transcript are retained in
`reference/q1.wav` and `reference/spoken.txt` for rebuilds.

New passages use the official `Qwen/Qwen3-TTS-12Hz-1.7B-Base` checkpoint pinned to
`fd4b254389122332181a7c3db7f27e918eec64e3`. A single reusable full reference prompt
keeps this synthetic voice across chapters. Chapter 2's columns scene reuses the
approved reference audio exactly because its spoken text is identical. No voice
belonging to a real person is used as a reference.

Install the requirements and a suitable CPU PyTorch/torchaudio build. The production environment uses CPU bfloat16, four Torch threads, and batches
of six passages, grouped by descending length. The initial three-scene batch is
retained in the cache. The six-scene longest batch produced 133.44 seconds of
audio in 811.13 seconds, with about 10 GB peak RSS. Use smaller batches on
machines with less memory. `download_model.py` verifies published model-file hashes and hardlinks
only hash-identical files from the existing VoiceDesign download. Model weights, raw generation and build files stay outside Git; the small
approved synthetic reference is retained with the source.

Create the environment in this order, installing the CPU packages before the
speech dependencies. These are the versions used for production; the complete
runtime versions are recorded in `runtime.json` and scene metadata.

```sh
python3.12 -m venv /tmp/qwen-venv
/tmp/qwen-venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch==2.15.0+cpu torchaudio==2.11.1+cpu
/tmp/qwen-venv/bin/pip install -r video/qwen-production/requirements.txt
/tmp/qwen-venv/bin/python -c "import torch,torchaudio; print(torch.__version__,torchaudio.__version__); assert torch.version.cuda is None; assert torchaudio.__version__.endswith('+cpu')"
/tmp/qwen-venv/bin/python video/qwen-production/download_model.py
/tmp/qwen-venv/bin/python video/qwen-production/synthesize.py --validate
# Inspect out/q1-validation/asr-00.json before full production.
/tmp/qwen-venv/bin/python video/qwen-production/synthesize.py
```

Default production destinations are `out/q1-chapter-01/`, `out/q1-chapter-02/`
and `out/q1-chapter-03/`. The chapter `synthesize.py` adapters also use these
isolated destinations. Set `EXPLAINER_OUT` only for a single chapter invocation.
Reference paths and the model directory can be set with `Q1_REFERENCE`,
`Q1_REFERENCE_TEXT`, and `--model-dir` respectively. Set `QWEN_BASE_MODEL` for the downloader when
using a model directory other than `/workspace/scratch/qwen-base/model`. Keep the original reference
bytes and transcript for a rebuild.

Each raw scene has content/model/reference hashes and generation metadata.
Independent unprompted Whisper `small.en` transcription is kept in `asr-NN.json`
with its real word timestamps, probabilities, original text and expected speech.
No vocabulary hint or digit suppression is used. Inspect these transcripts for
omissions, substitutions, negations, identifiers and numbers before rendering.

Qwen does not provide word boundaries. `words-NN.json` explicitly labels its
canonical-word timing as **ASR alignment to canonical spoken text**. Matching ASR
characters supply timing anchors; punctuation and numeric spelling are
normalised, and unmatched characters interpolate between adjacent anchors.
The file records differences, per-word matching coverage, and the explicit
`audio_time_offset_seconds` needed to locate words in padded scene audio. This
is estimated alignment, not forced alignment or proof that a canonical word was
spoken. No previous provider's timestamps are reused. No generated content is
trimmed from the raw speech. Captions and sentence cues preserve canonical text.

After inspecting the scene ASR, run the shared pronunciation pack before rendering:

```sh
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-01 --build out/q1-chapter-01
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-01 --build out/q1-chapter-01 --check
EXPLAINER_OUT="$PWD/out/q1-chapter-01" /tmp/qwen-venv/bin/python video/chapter-01/render.py
```

Repeat for each chapter. The pronunciation pack is automated screening and never
establishes a listening review. Preserve the pack, full ASR, scene audio, timing
files and source settings for review. Published `assets/video/` files are updated
only after independent review of the completed exports.

The completed export and scene provenance is retained in `production-manifest.json`;
chapter `review.md` files record actual durations, checks and recognition limits.
