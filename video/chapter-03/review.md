# Export review — 28 October 2026

Delivered export: **3:05**, 1280×720, 24 fps; 10 scenes; 46 selectable caption cues; five-second silent closing card. MP4 size: 4,769,069 bytes. SHA-256: `eb049f729eb2d05da3011c66fede41f2acb9a5be3820e6a02c7eccf522038092`.

## Checks performed

- Narration compared with Chapter 3: completed-only measure, the overlapping lineage/provenance definitions, F1300 → summary-R1205 → R1205 → S1205/completed-v1, 12:05 publication versus 13:00 refresh, and the retained-input calculation 2/2 = 100%. Recovery and currency remain Chapter 4's questions.
- Provider word alignment checked by the synthesis helper. Display captions concatenate exactly to the canonical narration; all 46 cue intervals are ordered and non-overlapping.
- Encoded frames from all ten scene clips visually reviewed. Long identifiers fit their cards; snapshot status and calculation inclusion have different headings. Reference arrows start from the producing run; investigation arrows are distinguished from processing flow. No customer records or external artwork are used.
- Full narration transcribed with faster-whisper `base.en`; isolated `small.en` checks covered definitions, refresh, publication, run and recap. Key numbers, negations and spoken identifiers agree. Full-track boundary repetitions did not recur in isolated passages. Homophones such as “our”/“R”, “root”/“route” and “red”/“read” remain transcription ambiguities, not evidence of different spoken words.
- ffprobe confirms H.264/yuv420p, AAC at 48 kHz, English mov_text captions and 184.958333 seconds of video versus 185.0 seconds of audio/container. Full FFmpeg decode passed.
- Embedded player checked in Chromium at 320, 768 and 1024 pixels, light and dark: no overflow or initial MP4 request, no autoplay, all 46 WebVTT cues load, seeking and playback work, and the player is hidden in print.
- All eleven chapter map activities checked at 320 and 900 pixels: chapter context, record example and field tabs, return to the exercise, collapsed answers and no JavaScript errors. SQLite examples, map records/layout, build and local links pass.

## SQLite pronunciation correction

The speech mapping originally expanded SQLite to “S Q Lite”, omitting the L. It now uses “sequel lite”. Only the opening speech was regenerated; hashes confirm that every other scene retains its original audio. The revised opening and an isolated final phrase were transcribed with `small.en`; the isolated check used no vocabulary prompt and recognised SQLite. Captions still spell the product name SQLite and were retimed for the shorter opening. The replacement MP4 passed full decoding, exact caption-text and timing checks, plus browser caption loading, seeking and playback. Automated recognition does not establish a listening review.

## Limits and retained material

No human listening review was performed. Automated transcription is an additional check, not a guarantee of pronunciation or prosody. The embedded player identifies the invented example and synthetic voice and offers captions and a transcript.

The source, narration, scene plan and settings are committed under `video/chapter-03/`. Final media is under `assets/video/chapter-03/`. Working audio, provider boundaries, timings, layers, clips, frames and audit reports remain in ignored `out/chapter-03/`; preserve these when making visual-only corrections.
