# Chapter 1 explainer video

A standalone narrated adaptation of [What the data cannot tell you](../../chapters/01-why-metadata.md). The same four parcels explain completed-delivery and all-due denominators, a recorded definition, ambiguous field meaning and checking a calculation.

Production follows the [authored video workflow](https://github.com/snowch/explainer-video-generator/blob/20ef33571f5b737c4fa267427964593836182205/docs/agent-video-workflow.md). Speech synthesis and audio-audit helpers are adapted from that repository's `examples/approved-narration/`; the renderer and scene plan are specific to this chapter. No reference-video artwork or unrelated narrative is reused.

## Inputs

- `narration.json`: exact display narration, in complete scene passages.
- `project.json`: source, attribution, voice, pronunciation and duration contract.
- `scene-plan.md`: chapter-to-scene source trail and visual interpretation checks.
- `render.py`: coded parcel/building illustrations, staged highlights and layouts.
- `synthesize.py`: cached scene speech, provider word boundaries, sentence cues and captions.
- `audit_audio.py`: automated transcription; it does not establish a listening review.

The source is pinned to metadata-book commit `46e8224334d69d9ef9eee103f0b4def368a9f807`. The optional historical-cutoff discussion is omitted from narration; the complete-record assumption is stated explicitly. No actual customer records appear.

## Rebuild

Use Python 3.12, FFmpeg/ffprobe and the DejaVu fonts specified in `project.json`. From the repository root:

```sh
python3 -m venv /tmp/metadata-video-venv
/tmp/metadata-video-venv/bin/pip install -r video/chapter-01/requirements.txt
/tmp/metadata-video-venv/bin/python video/chapter-01/synthesize.py
/tmp/metadata-video-venv/bin/python video/chapter-01/render.py
```

The default output is ignored `out/chapter-01/`. Set `EXPLAINER_OUT` to the same absolute build directory for both commands to change it. Keep scene audio, word metadata, timings, layers and independent clips for corrections. The speech cache includes spoken text, voice, rate, provider version and boundary mode. The visual cache includes renderer source, scene timing, configuration and fonts.

The online speech client uses `HTTPS_PROXY` when configured. It adds the environment's trusted CA bundle (`SSL_CERT_FILE`, or `/etc/ssl/certs/ca-certificates.crt`) while retaining TLS verification. No service credential is stored. Hosted speech may change; preserve the rendered audio for reproducible visual edits.

Outputs include `chapter-01.mp4`, `captions.srt`, `captions.vtt`, `transcript.txt`, `narration.wav` and `timings.json`. Video is 1280×720, 24 fps, H.264/yuv420p, AAC with selectable English captions and faststart. Captions are also provided separately. No permanent subtitle strip or music is used.

## Review

```sh
/tmp/metadata-video-venv/bin/pip install -r video/chapter-01/requirements-audit.txt
/tmp/metadata-video-venv/bin/python video/chapter-01/audit_audio.py
/tmp/metadata-video-venv/bin/python video/chapter-01/audit_audio.py --model small.en --scenes 1,2,8
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,duration -of json out/chapter-01/chapter-01.mp4
ffmpeg -hide_banner -loglevel error -i out/chapter-01/chapter-01.mp4 -f null -
```

Audit downloads Whisper weights on first use. Inspect exported frames, full and isolated transcription, negations and percentages. Digit suppression may distort number recognition, so investigate a discrepancy with normal numeral decoding too. ASR is not a phonetic guarantee. Source checks and visual meaning review are manual.

For a partial visual rebuild, `render.py --only 1 --no-mux` renders only scene 1. It deliberately does not remux a possibly stale full sequence. For a full render the cache skips unchanged clips. After editing narration or pronunciation, rebuild timings and review the resulting captions before the complete export.

## Sharing and embedding

Keep generated media and model weights out of git. The delivered MP4, captions, poster and transcript can be hosted together on the chosen media host. A local `watch.html` is supplied with the export for preview through a static HTTP server. It uses playback controls, WebVTT captions, a transcript link, and a visible invented-example and synthetic-voice disclosure. No autoplay is enabled. Verify actual media URLs before adding an embed to the published chapter.

See `out/chapter-01/review.md` for the measured result and checks performed on this export. No human listening review is claimed.
