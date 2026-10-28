# Export review — 28 October 2026

Delivered export: **3:08**, 1280×720, 24 fps; 12 scenes; 50 selectable caption cues; five-second silent closing card. MP4 size: 5,019,138 bytes. SHA-256: `9d1b27f0d386b95eb9f428364614de0f9d161c756cb09c0646a7292f7f8e8c67`.

## Checks performed

- Narration manually compared with Chapter 1. Both denominator calculations, the complete-record assumption, invented-example disclosure and all three core points preserved. The optional late-update discussion is outside this short video's scope.
- Provider word boundaries match the pronunciation-expanded script. Display captions concatenate exactly to the canonical narration; 50 cue intervals are ordered and non-overlapping. Short trailing fragments were rebalanced at phrase boundaries where possible.
- Complete definition shown with noon deadline distinct from 13:00 UTC measurement, responsible team and source table. The fourth parcel stays visible outside the completed-only bracket and inside the all-due bracket.
- Actual encoded frames from all twelve scene clips reviewed together, including the opening, both denominators, full definition, alternative meanings and close. A wrapped heading was corrected. Clips are copied into the MP4 without video re-encoding. Selected final MP4 frames were extracted too.
- Full generated audio transcribed with faster-whisper `base.en`, CPU/int8, with voice-activity detection. Isolated `small.en` checks covered percentage scenes and apparent full-track boundary repetitions. “Reviewer,” “denominator,” `delivered_at`, the complete definition and closing qualifications were checked against their source text.
- Initial hyphenated speech input `sixty-six` was repeatedly recognised as “six to six.” A separately generated unhyphenated sample was recognised as `66.7%`; the final explicit pronunciation is `sixty six point seven percent`. The completed-delivery and mismatch scenes were regenerated. Isolated final recognition returned “sixty-six point seven percent” for both, and “fifty percent” for the all-due result. Display text remains `66.7%` / `50.0%`.
- ffprobe confirms H.264/yuv420p video, AAC audio, English mov_text captions and audio/video durations differing by 42 milliseconds: video 187.958333 seconds, audio/container 188.0 seconds. Full FFmpeg decode passed.
- Local preview checked in Chromium at 390 and 1024 pixels: no page overflow, media loads, seeking works, all 50 WebVTT cues load, playback controls and visible example disclosure present.
- Book build, SQLite examples, map data/layout and local links still pass.

## Limits and retained material

No human listening review was performed. Transcription can misrecognise words or repeat them at segment boundaries; it is an additional check, not a guarantee of pronunciation or prosody. A voice preview is included for the viewer. This video has not been embedded in the published chapter or uploaded to a media host.

The ignored `out/chapter-01/` build keeps raw and padded scene audio, provider word boundaries, timings, layers, independently encoded clips, captions, transcript, frames, contact sheet and audit reports. The viewing package contains the final MP4, SRT, WebVTT, transcript, poster, voice preview, review and a local preview page. The source package contains the script, scene plan, settings, pinned dependencies and rebuild helpers.
