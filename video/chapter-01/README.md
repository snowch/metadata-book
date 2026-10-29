# Chapter 1 explainer video

A standalone narrated adaptation of [What the data cannot tell you](../../chapters/01-why-metadata.md). The same four parcels explain completed-delivery and all-due denominators, a recorded definition, ambiguous field meaning and checking a calculation.

Production follows the [authored video workflow](https://github.com/snowch/explainer-video-generator/blob/20ef33571f5b737c4fa267427964593836182205/docs/agent-video-workflow.md). Speech synthesis and audio-audit helpers are adapted from that repository's `examples/approved-narration/`; the renderer and scene plan are specific to this chapter. No reference-video artwork or unrelated narrative is reused.

## Inputs

- `narration.json`: exact display narration, in complete scene passages.
- `project.json`: source, attribution, voice, pronunciation and duration contract.
- `scene-plan.md`: chapter-to-scene source trail and visual interpretation checks.
- `render.py`: coded parcel/building illustrations, staged highlights and layouts.
- `synthesize.py`: cached scene speech, fresh ASR alignment estimates, sentence cues and captions.
- `audit_audio.py`: automated transcription; it does not establish a listening review.

The source is pinned to metadata-book commit `46e8224334d69d9ef9eee103f0b4def368a9f807`. The optional historical-cutoff discussion is omitted from narration; the complete-record assumption is stated explicitly. No actual customer records appear.

## Rebuild

Use Python 3.12, FFmpeg/ffprobe and the DejaVu fonts specified in `project.json`. Create the CPU environment in the install order documented in the [Q1 production instructions](../qwen-production/README.md), then run from the repository root:

```sh
export EXPLAINER_OUT="$PWD/out/q1-chapter-01"
/tmp/qwen-venv/bin/python video/chapter-01/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-01 --build "$EXPLAINER_OUT"
# Review out/q1-chapter-01/pronunciation-audit/index.html before rendering.
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-01 --build "$EXPLAINER_OUT" --check
/tmp/qwen-venv/bin/python video/chapter-01/render.py
```

The default output is ignored `out/q1-chapter-01/`. Set `EXPLAINER_OUT` to the same absolute build directory for both commands to change it. Keep scene audio, word metadata, timings, layers and independent clips for corrections. The speech cache verifies raw audio hashes and records spoken text, model/reference hashes, SDK versions, seed and batch membership. Word timing is a fresh ASR estimate with matching coverage recorded. The visual cache includes renderer source, scene timing, configuration and fonts.

Speech uses the local pinned Qwen Base model and the approved synthetic Q1 reference. See the [Q1 production instructions](../qwen-production/README.md) for model download, reference provenance, caching and alignment limitations.

Outputs include `chapter-01.mp4`, `captions.srt`, `captions.vtt`, `transcript.txt`, `narration.wav` and `timings.json`. Video is 1280×720, 24 fps, H.264/yuv420p, AAC with selectable English captions and faststart. Captions are also provided separately. No permanent subtitle strip or music is used.

## Pronunciation audit before rendering

Follow the [pronunciation audit workflow](../README.md#audit-pronunciation-after-generating-narration) after generating speech. The shared helper extracts technical-term clips and transcribes them without vocabulary hints. Review the intended pronunciations, inspect differences, and record any unresolved terms. A spelling match is not proof of pronunciation.

## Review

```sh
/tmp/qwen-venv/bin/python video/chapter-01/audit_audio.py
/tmp/qwen-venv/bin/python video/chapter-01/audit_audio.py --model small.en --scenes 1,2,8
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,duration -of json out/q1-chapter-01/chapter-01.mp4
ffmpeg -hide_banner -loglevel error -i out/q1-chapter-01/chapter-01.mp4 -f null -
```

Audit downloads Whisper weights on first use. Inspect exported frames, full and isolated transcription, negations and percentages. Digit suppression may distort number recognition, so investigate a discrepancy with normal numeral decoding too. ASR is not a phonetic guarantee. Source checks and visual meaning review are manual.

For a partial visual rebuild, `render.py --only 1 --no-mux` renders only scene 1. It deliberately does not remux a possibly stale full sequence. For a full render the cache skips unchanged clips. After editing narration or pronunciation, rebuild timings and review the resulting captions before the complete export.

## Sharing and embedding

Chapter 1 embeds the final MP4, captions, poster and transcript from `assets/video/chapter-01/`, published with the book. This deliberate final-media copy is about 5 MB; working audio, clips, generated layers and model weights remain outside git. A local `watch.html` is supplied with the export for preview through a static HTTP server. It uses playback controls, WebVTT captions, a transcript link, and a visible invented-example and synthetic-voice disclosure. No autoplay is enabled. The chapter embed uses `preload="none"` so the video is not fetched until requested; the poster and resource links remain visible. Check actual media URLs after each publication.

See `out/q1-chapter-01/review.md` for the measured result and checks performed on this export. No human listening review is claimed.
