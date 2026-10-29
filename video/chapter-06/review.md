# Chapter 6 learning-aid review — 29 October 2026

Source: `f8bb703316888ca0fcdb78d728e0f0b5381bbb18`. Guidance: explainer
`f16d0350df20cb35681886cb5d197ce27f2d3a49`. Audience: report readers and
engineers. Objective: Explain why duplicate, delayed, missing and conflicting records need different evidence before changing current state.

Free workspace disk space before starting: 25 GB available (19% used). Checked with `df -h /workspace`.

## Export and speech

2:42 (162.300 seconds), 1280×720 at 24 fps, H.264/yuv420p,
AAC and selectable English captions. 46 cues; 4,413,929 bytes.
SHA-256: `93d48ca6d541cb45a68855a0dac1b5120d47dab3458f7c897749e8426a42286d`.

Approved original synthetic Q1 reference and pinned Qwen Base model. Complete
passages retained without generated-word trimming or tempo alteration. Original
independent, unprompted small.en ASR is separate from canonical text and estimated
alignment. Matched-character coverage 95.3–100.0%.
Pronunciation pack: 17 contextual excerpts, 5
text mismatches. Full-scene differences are number formatting, are/our identifier homophones, catalogue/catalog, labelled/labeled and recognised/recognizing spelling. The 17 term clips include five text mismatches involving catalogue or formatted identifiers. Full context preserves E20/E19, R1000/R0950, summary versions, event/receipt times, negations and the unresolved conflict. No phonetic approval is inferred.

**No human listening review was performed.** Recognition screens words and
identifiers; it does not certify phonetics, accent, naturalness or delivery.
Reader understanding, engagement, delayed recall and transfer outcomes are
**not assessed**; the rubric below records design/source/export judgments.

## Learning-aid rubric

| Criterion | Finding and evidence |
|---|---|
| Alignment and relevance | Meets source/design review: missing, duplicate, delayed and conflicting evidence retain distinct consequences. |
| Clarity | Design review: absence and conflicting-publication questions receive separate explicit answers; reader understanding unassessed. |
| Visual explanation | Meets encoded-frame review: crossed event/receipt timeline and later duplicate-receipt reveal clarify chronology and identity. |
| Focus and memorability | Design review: preserve claims and show uncertainty; delayed recall unassessed. |
| Active recall | Meets export review: two four-second holds; no deletion answer or winning source leaked in graphics/captions. |
| Application and page connection | Meets tested scope: Source observation → Collection run map activity opens; later omission is hypothetical, then page feedback. |
| Cognitive load and pacing | Design review: short evidence excerpts with full records retained on page; separate 20/21 October examples labelled. |
| Engagement | Design judgment: consequential questions and visibly crossed chronology invite inspection; viewer engagement unassessed. |
| Accuracy | Meets source review: stable source/event ID, reported versus proven publication, different failed run, clock-order qualification and disputed state preserved. |
| Accessibility and control | Meets tested scope: labels plus colour, transcript/captions, inspected phone frame and 960/390px playback; user accessibility study unassessed. |
| Series progression | Meets design review: builds on Chapter 5 collection evidence to decide which conclusions it warrants. |

## Completed checks

- Pronunciation-pack freshness and excerpt hashes; complete scene ASR inspected separately.
- Full FFmpeg decode, expected media streams, synchronized durations and five-second end card.
- Canonical caption text preserved, ordered and non-overlapping. Both four-second response holds have no active captions; exported audio silence checked with an AAC boundary margin.
- Actual encoded scene frames, response holds, staged reveals and phone rendering inspected.
- Chromium playback, seeking, captions, response holds, no overflow and linked map Example record at 960px and 390px; no page errors.
- Repeated packaging is idempotent: one page embed and manifest entry; previous chapters' provenance and original page prose preserved.
- Pronunciation unit tests, SQLite/example checks, map data/layout validation, full site build and `git diff --check` pass.

Working evidence remains in ignored `out/q1-chapter-06/`: raw speech and
provenance, original ASR, alignment, pronunciation clips, timings, captions,
encoded frames, media and browser reports. Publication is checked after merge.
