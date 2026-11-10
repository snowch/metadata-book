# Chapter 1: choose what counts

This replacement pairs a responsive interactive parcel lab, an eight-slide PDF
and a native 4K browser recording. Approved talk track: `scenes.json`.
`assets/lessons/chapter-01/` contains the shared lab/deck design, not screenshots
of a separate presentation. The lab supplies a worked example, a guided choice
and an independent six-parcel example with denominator feedback.

The recording uses `snowch/claude-skills` at
`c9a7c521568632aa216932f4c965df386498602a` (Linux support, PR #3), Kokoro v1.0
ONNX CPU, `af_heart`, speed 1.0. This is a new voice/backend replacing the previous
Q1 recording. Model/voice hashes, source commit and final assets are in
`production.json`. Font: Source Sans 3, bundled with its OFL license.

Rebuild with Python 3.12, FFmpeg, Chromium, uv, and the recording skill checkout:

```sh
mkdir -p out/chapter-01-v2
cp video/chapter-01-v2/{scenes.json,tour.py} out/chapter-01-v2/
# Serve the repository root on localhost:8031 in another terminal.
python -m http.server 8031 --directory .
```

Set `RECORD_SCRIPTS` to the recording skill's `scripts` directory, then run:

```sh
uv run "$RECORD_SCRIPTS/tts.py" out/chapter-01-v2 af_heart 1.0
uv run "$RECORD_SCRIPTS/phonemes.py" out/chapter-01-v2 --all
uv run "$RECORD_SCRIPTS/asr.py" out/chapter-01-v2 small.en
uv run "$RECORD_SCRIPTS/record.py" out/chapter-01-v2 http://127.0.0.1:8031
DEMO_FFMPEG_PRESET=veryfast uv run "$RECORD_SCRIPTS/build.py" out/chapter-01-v2 chapter-01
uv run --with playwright --with pypdf --with Pillow video/chapter-01-v2/export_deck.py
uv run --with faster-whisper --with soundfile --with numpy --with num2words video/chapter-01-v2/captions.py
```

Review ASR originals and actual encoded frames before packaging. `captions.py`
uses independent ASR anchors aligned to canonical text; those timings are
estimates, not provider timestamps. Question holds follow speech and captions.
The final mux copies video/audio and replaces only subtitle text/timing.

Publish `chapter-01-4k-silent.mp4` as `chapter-01-silent.mp4`, the remuxed narrated
copy as `chapter-01.mp4`, the PDF as `deck.pdf`, SRT/VTT and a poster under
`assets/video/chapter-01-v2/`. `package.py` refreshes content hashes, transcript,
page links and provenance once those files exist. It does not publish remotely.
The page uses a scoped stylesheet, leaving other lessons' presentation intact.
See `review.md` for completed checks and limits. Do not regenerate unchanged
speech for a visual correction. Retain working audio, frames and ASR under `out/`.

## Picture-only simplification

The current picture removes recording chrome, timestamps, grouping labels and
explanatory paragraphs. `visuals.json` defines the single heading and calculation
cue for each scene. `simplify_visuals.py` renders native 4K browser states against
the retained frame timeline, including the parcel transition and later calculation
reveal. It remuxes the original audio/subtitle streams, then checks their packet
hashes and timestamps. The bottom 144px of the 720px layout stays empty.

Run it with Playwright installed and the repository served on localhost:8031.
Retain `out/chapter-01-v2/timeline.json` and `audio/*.asr.json` from the approved
recording. `export_deck.py` uses the same simplified headings and final states.
This correction changes picture and layout; it does not regenerate speech.
