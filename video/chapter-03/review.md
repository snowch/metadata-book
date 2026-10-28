# Export review — 28 October 2026

Delivered export: **3:05**, 1280×720, 24 fps; 10 scenes; 46 selectable caption cues; five-second silent closing card. MP4 size: 4,766,447 bytes. SHA-256: `02fb469370ef333b5f9c39d791cde83fa17327ba82f40848a32cc6decba747d1`.

## Checks performed

- Narration compared with Chapter 3: completed-only measure, the overlapping lineage/provenance definitions, F1300 → summary-R1205 → R1205 → S1205/completed-v1, 12:05 publication versus 13:00 refresh, and the retained-input calculation 2/2 = 100%. Recovery and currency remain Chapter 4's questions.
- Provider word alignment checked by the synthesis helper. Display captions concatenate exactly to the canonical narration; all 46 cue intervals are ordered and non-overlapping.
- Encoded frames from all ten scene clips visually reviewed. Long identifiers fit their cards; snapshot status and calculation inclusion have different headings. Reference arrows start from the producing run; investigation arrows are distinguished from processing flow. No customer records or external artwork are used.
- Full narration transcribed with faster-whisper `base.en`; isolated `small.en` checks covered definitions, refresh, publication, run and recap. Key numbers, negations and spoken identifiers agree. Full-track boundary repetitions did not recur in isolated passages. Homophones such as “our”/“R”, “root”/“route” and “red”/“read” remain transcription ambiguities, not evidence of different spoken words.
- ffprobe confirms H.264/yuv420p, AAC at 48 kHz, English mov_text captions and 185.125 seconds of video versus 185.2 seconds of audio/container. Full FFmpeg decode passed.
- Embedded player checked in Chromium at 320, 768 and 1024 pixels, light and dark: no overflow or initial MP4 request, no autoplay, all 46 WebVTT cues load, seeking and playback work, and the player is hidden in print.
- All eleven chapter map activities checked at 320 and 900 pixels: chapter context, record example and field tabs, return to the exercise, collapsed answers and no JavaScript errors. SQLite examples, map records/layout, build and local links pass.

## Limits and retained material

No human listening review was performed. Automated transcription is an additional check, not a guarantee of pronunciation or prosody. The embedded player identifies the invented example and synthetic voice and offers captions and a transcript.

The source, narration, scene plan and settings are committed under `video/chapter-03/`. Final media is under `assets/video/chapter-03/`. Working audio, provider boundaries, timings, layers, clips, frames and audit reports remain in ignored `out/chapter-03/`; preserve these when making visual-only corrections.
