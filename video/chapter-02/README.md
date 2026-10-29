# Chapter 2 explainer video

An authored adaptation of [What a database already knows](../../chapters/02-reading-a-database.md), with actual structural metadata and SQL from the invented delivery example. Source commit is pinned in `project.json`. The renderer is chapter-specific Pillow artwork with FFmpeg fades and muxing; speech and audit helpers follow the existing Chapter 3 workflow.

The production contract is `narration.json`, `project.json` and `scene-plan.md`. Review the source script before synthesis. After synthesis, review pronunciation before rendering. Original synthetic Q1 British female voice, 1280×720, 24 fps, cream/rust/green visuals, no music, selectable English captions and a five-second end card.

With FFmpeg and DejaVu fonts installed, create the CPU environment in the install order documented in the [Q1 production instructions](../qwen-production/README.md), then run from the repository root:

```sh
export EXPLAINER_OUT="$PWD/out/q1-chapter-02"
/tmp/qwen-venv/bin/python video/chapter-02/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-02 --build "$EXPLAINER_OUT"
# Inspect intended speech and audit clips; record the review method and concerns.
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-02 --build "$EXPLAINER_OUT" --check
/tmp/qwen-venv/bin/python video/chapter-02/preview.py
/tmp/qwen-venv/bin/python video/chapter-02/render.py
/tmp/qwen-venv/bin/python video/chapter-02/audit_audio.py
```

`preview.py` composes timed scene PNGs and a contact sheet without video encoding, for checking layout before rendering.

Working outputs are ignored `out/q1-chapter-02/`. Set `EXPLAINER_OUT` for the chapter scripts and pass `--build` to the shared pronunciation audit when using another build directory. Outputs include `chapter-02.mp4`, `narration.wav`, `captions.srt`, `captions.vtt`, `transcript.txt`, timings, ASR alignment estimates, layers and scene clips. Hash-verified raw-scene caching preserves unaffected speech after corrections. ASR transcripts and estimated canonical-word timing are retained separately. Visual cache signatures include the renderer, fonts, configuration and scene timings. `--only 4 --no-mux` supports partial visual correction; full rendering reuses unchanged clips.

Speech uses the local pinned Qwen Base model and approved synthetic Q1 reference. See the [Q1 production instructions](../qwen-production/README.md) for model download, reference provenance and alignment limitations.

The [shared pronunciation workflow](../README.md) is mandatory after synthesis and before rendering, including after pronunciation changes. Automated ASR is not proof that a term sounds correct; do not claim a listening review without one. Final content, visual, caption and playback checks are also required. Synthesis and rendering do not publish; the explicit packaging step below copies final media locally.

`preview.py` composes static PNGs and a contact sheet from the real timings without encoding video. Use it for visual review before the full render. The [export review](review.md) records the checks and limitations for the published version. Final media is embedded in Chapter 2 from `assets/video/chapter-02/`, with no autoplay or MP4 preload, captions and a transcript. `watch.html` can be copied alongside the exported media for a local preview.

## Page learning aid revision

The new script reinforces structure versus meaning and the saved query's filter.
It includes two four-second prediction holds and returns to the existing page
exercise. Full SQL and the catalogue comparison remain on the page. The renderer
uses `../learning_aid.py`; the Q1 speech workflow is unchanged. After the standard
pronunciation check and render, run the shared `verify_learning_aid.py`,
`package_learning_aid.py` and `verify_learning_aid_browser.py` with `--chapter 02`,
as documented in `video/README.md`. See `review.md` for actual export evidence.
