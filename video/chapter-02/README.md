# Chapter 2 explainer video

An authored adaptation of [What a database already knows](../../chapters/02-reading-a-database.md), with actual structural metadata and SQL from the invented delivery example. Source commit is pinned in `project.json`. The renderer is chapter-specific Pillow artwork with FFmpeg fades and muxing; speech and audit helpers follow the existing Chapter 3 workflow.

The production contract is `narration.json`, `project.json` and `scene-plan.md`. Review the source script before synthesis. After synthesis, review pronunciation before rendering. British Sonia voice, 1280×720, 24 fps, cream/rust/green visuals, no music, selectable English captions and a five-second end card.

From the repository root, with FFmpeg and DejaVu fonts installed:

```sh
/tmp/metadata-video-venv/bin/pip install -r video/chapter-02/requirements-audit.txt
/tmp/metadata-video-venv/bin/python video/chapter-02/synthesize.py
/tmp/metadata-video-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-02
# Inspect intended speech and audit clips; record the review method and concerns.
/tmp/metadata-video-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-02 --check
/tmp/metadata-video-venv/bin/python video/chapter-02/preview.py
/tmp/metadata-video-venv/bin/python video/chapter-02/render.py
/tmp/metadata-video-venv/bin/python video/chapter-02/audit_audio.py
```

`preview.py` composes timed scene PNGs and a contact sheet without video encoding, for checking layout before rendering.

Working outputs are ignored `out/chapter-02/`. Set `EXPLAINER_OUT` for the chapter scripts and pass `--build` to the shared pronunciation audit when using another build directory. Outputs include `chapter-02.mp4`, `narration.wav`, `captions.srt`, `captions.vtt`, `transcript.txt`, timings, word boundaries, layers and scene clips. Provider caching preserves other scenes after speech corrections. Visual cache signatures include the renderer, fonts, configuration and scene timings. `--only 4 --no-mux` supports partial visual correction; full rendering reuses unchanged clips.

Synthesis retains TLS verification, adds the configured trust bundle and uses `HTTPS_PROXY` when present. No credentials are stored. Preserve generated speech if exact reproducibility is needed: hosted speech can change.

The [shared pronunciation workflow](../README.md) is mandatory after synthesis and before rendering, including after pronunciation changes. Automated ASR is not proof that a term sounds correct; do not claim a listening review without one. Final content, visual, caption and playback checks are also required. No publication or final-media copy is performed by these source scripts.

`preview.py` composes static PNGs and a contact sheet from the real timings without encoding video. Use it for visual review before the full render. The [export review](review.md) records the checks and limitations for the published version. Final media is embedded in Chapter 2 from `assets/video/chapter-02/`, with no autoplay or MP4 preload, captions and a transcript. `watch.html` can be copied alongside the exported media for a local preview.
