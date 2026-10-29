# Chapter 1 page-learning-aid review — 29 October 2026

Replaces the standalone summary with a focused denominator demonstration, two
retrieval pauses, and a return to the page's metric-definition/map exercise.
The full metric record, metadata definition and field-name discussion remain on
the page. Source: `476c510abafeb8fc94a847b43595d3ae0d21e487`.

## Actual export

2:23 (142.8 seconds), 1280×720, 24 fps, H.264/yuv420p, AAC and selectable English
captions. 39 caption cues; 3,869,754 bytes. Video SHA-256:
`7e12b061b56bbbc3156a926f28f83d752f8feba4b91a6f20f515879e36f92d85`.
The approved original synthetic Q1 reference and pinned Qwen Base model are
retained. No speech tempo alteration. Nine new complete narration passages.

## Learning and source review

Manually compared the script and each visual with Chapter 1. The two on-time
parcels remain the numerator; the late arrival belongs to completed deliveries;
the unfinished parcel remains visible while the denominator expands from three
to four. Both percentages are valid for their stated questions. Only Delivery
Operations' all-due definition requires 50.0%. Definition excerpts name the
measurement time and responsible team; they do not claim to replace the full
record or prove implementation correctness. Questions precede their answer
scenes. The final activity uses the existing Metric definition → Example record
route and page answer.

## Speech screening

Independent full-scene unprompted small.en ASR preserves the narration's numbers,
questions, negation and qualifications. Alignment coverage is 100% except the
rule passage (99.1%): “all-due” is recognised as “all-do”, a homophone spelling
difference. A short term clip writes “all-day”; full-scene context is retained
for inspection. Other short excerpts include boundary hallucinations; these
were checked against full-scene recognition rather than treated as extra spoken
words. The pronunciation pack has 11 clips and three transcription differences,
including 50.0% rendered as “50 percent”. Its freshness check passed before
rendering. Recognition does not establish phonetic correctness.

**No human listening review was performed.** Voice expressiveness and precise
pronunciation remain screened rather than listening-approved. No learner study
or delayed-recall test has been performed; retrieval opportunities are design
choices, not measured learning gains.

## Completed checks

- Full FFmpeg decode; video/audio duration agreement, expected streams and five-second closing hold.
- All captions concatenate exactly to the canonical narration; ordered, non-overlapping cues.
- Four- and five-second response holds leave 4.592 and 5.630 seconds after the last caption, respectively.
- Inspected actual encoded frames for every scene, both response holds and a 390-pixel rendering; no clipping or answer shown during thinking time.
- Chromium at 960px and 390px: playback advances, seeking works, captions load, response holds have no active caption, no page overflow, and the map's Example record opens.
- Existing pronunciation-audit tests, SQL/example checks, metadata-map validation, layout consistency and complete site build pass.

Evidence remains in ignored `out/q1-chapter-01/`: raw scene audio and model
metadata, independent ASR, aligned words, pronunciation pack, timings, encoded
frames/contact sheet, media-verification.json, browser-verification.json and
browser screenshots. The committed production manifest retains scene provenance.
