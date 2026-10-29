# Chapter 9 learning-aid review — 29 October 2026

Source: `eec9cf06927910c7eef2b73e437a03430d023cbb`. Guidance: explainer
`f16d0350df20cb35681886cb5d197ce27f2d3a49`. Audience: report readers and
engineers. Objective: Separate event format, delivery configuration and explicit identity mappings, and identify evidence missing from a completion event.

Free workspace disk space before starting: 25 GB available (19% used). Checked with `df -h /workspace`.

## Export and speech

2:23 (142.800 seconds), 1280×720 at 24 fps, H.264/yuv420p,
AAC and selectable English captions. 38 cues; 3,865,790 bytes.
SHA-256: `7bf0def5ff12e88094526561400c8042250933322ea25752d8228e263de1c988`.

Approved original synthetic Q1 reference and pinned Qwen Base model. Complete
passages retained without generated-word trimming or tempo alteration. Original
independent, unprompted small.en ASR is separate from canonical text and estimated
alignment. Matched-character coverage 99.1–100.0%.
Pronunciation pack: 20 contextual excerpts, 5
text mismatches. Full-scene ASR preserves JSON/HTTP, UUID lifecycle, the R1205 correspondence, transport qualifications and the missing evidence. Alignment differences are catalogue/catalog, acknowledgement/acknowledgment and 12.05 number formatting. The 20 excerpts have five mismatches: JSON as Jason, R1205 numeric/letter spellings and catalogue/catalog; short boundary words can be cut or misrecognised. Full passages were consulted; original ASR remains unchanged and phonetics unapproved.

**No human listening review was performed.** Recognition screens words and
identifiers; it does not certify phonetics, accent, naturalness or delivery.
Reader understanding, engagement, delayed recall and transfer outcomes are
**not assessed**; the rubric below records design/source/export judgments.

## Learning-aid rubric

| Criterion | Finding and evidence |
|---|---|
| Alignment and relevance | Meets source/design review: event format, configured delivery and explicit identity mappings remain separate. |
| Clarity | Design review: connection and name-collision questions receive later explicit answers; reader understanding unassessed. |
| Visual explanation | Meets encoded-frame review: incomplete route question, transport/acceptance/retrieval path and progressively revealed identity mappings. |
| Focus and memorability | Design review: compatible format is not a connected evidence chain; delayed recall unassessed. |
| Active recall | Meets export review: two silent holds; connection configuration and namespace/UUID answers follow in later scenes. |
| Application and page connection | Meets tested scope: Run → Job; identify absent namespace/exchange UUID, then use page feedback. |
| Cognitive load and pacing | Design review: short identity excerpts replace full JSON/UUID on screen; exact event and configuration stay on page. |
| Engagement | Design judgment: concrete connection and name-collision problems invite investigation; viewer engagement unassessed. |
| Accuracy | Meets source review: sourced completion claim, missing retained versions, UUID lifecycle, dataset mapping, acknowledgement/query distinction and separate query standard preserved. |
| Accessibility and control | Meets tested scope: labels and arrows, acronym expansions, transcript/captions, inspected phone frame and 960/390px browser playback; no accessibility user study. |
| Series progression | Meets design review: extends collection and identity lessons to crossing system boundaries without claiming exactly-once delivery. |

## Completed checks

- Pronunciation-pack freshness and excerpt hashes; complete scene ASR inspected separately.
- Full FFmpeg decode, expected media streams, synchronized durations and five-second end card.
- Canonical caption text preserved, ordered and non-overlapping. Both four-second response holds have no active captions; exported audio silence checked with an AAC boundary margin.
- Actual encoded scene frames, response holds, staged reveals and phone rendering inspected.
- Chromium playback, seeking, captions, response holds, no overflow and linked map Example record at 960px and 390px; no page errors.
- Repeated packaging is idempotent: one page embed and manifest entry; previous chapters' provenance and original page prose preserved.
- Pronunciation unit tests, SQLite/example checks, map data/layout validation, full site build and `git diff --check` pass.

Working evidence remains in ignored `out/q1-chapter-09/`: raw speech and
provenance, original ASR, alignment, pronunciation clips, timings, captions,
encoded frames, media and browser reports. Publication is checked after merge.
