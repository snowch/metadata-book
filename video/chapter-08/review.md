# Chapter 8 learning-aid review — 29 October 2026

Source: `4f683bc967c1cdd8674a7d8b2fa83337f9760369`. Guidance: explainer
`f16d0350df20cb35681886cb5d197ce27f2d3a49`. Audience: report readers and
engineers. Objective: Assess a bounded pilot using accessible evidence, limited coverage and ongoing maintenance thresholds.

Free workspace disk space before starting: 25 GB available (19% used). Checked with `df -h /workspace`.

## Export and speech

2:28 (148.000 seconds), 1280×720 at 24 fps, H.264/yuv420p,
AAC and selectable English captions. 42 cues; 4,065,445 bytes.
SHA-256: `c7ef1d70967ce69df3cbc6444df15c9e0f74d48b057a90832ddd043931d4de49`.

Approved original synthetic Q1 reference and pinned Qwen Base model. Complete
passages retained without generated-word trimming or tempo alteration. Original
independent, unprompted small.en ASR is separate from canonical text and estimated
alignment. Matched-character coverage 98.7–100.0%.
Pronunciation pack: 13 contextual excerpts, 3
text mismatches. Full-scene ASR preserves the evidence chain, 90-minute/two-hour comparison, one-day threshold, scope and ownership qualifications. SQLite is rendered as esquilite in both full and excerpt ASR; exact phonetics remain unresolved without listening. The other two excerpt mismatches are catalogue/catalog spelling. Alignment also records an inserted one in the coverage question although the full transcript expresses the intended one-week pilot. Original recognition remains unchanged.

**No human listening review was performed.** Recognition screens words and
identifiers; it does not certify phonetics, accent, naturalness or delivery.
Reader understanding, engagement, delayed recall and transfer outcomes are
**not assessed**; the rubric below records design/source/export judgments.

## Learning-aid rubric

| Criterion | Finding and evidence |
|---|---|
| Alignment and relevance | Meets source/design review: bounded evidence tasks, accessible records and maintenance/freshness thresholds. |
| Clarity | Design review: collector coverage and platform choice questions receive later explicit answers. |
| Visual explanation | Meets encoded-frame review: evidence chain, proportional 90/120-minute bar and later trial-threshold reveal. |
| Focus and memorability | Design review: test the smallest arrangement within known limits; delayed recall unassessed. |
| Active recall | Meets export review: missing evidence and scoped choice questions have silent holds; no answers shown early. |
| Application and page connection | Meets tested scope: Collection run → Responsible team exercise and page feedback; map supplies no pilot effort measurements. |
| Cognitive load and pacing | Design review: pilot comparisons enlarged; full assessment/product documentation remains on page. |
| Engagement | Design judgment: concrete go/continue/trial decision rewards inspecting budget and scope; viewer engagement unassessed. |
| Accuracy | Meets source review: invented outcome labelled, tested access scope qualified, manual gaps retained, neither product nor wider sources assessed. |
| Accessibility and control | Meets tested scope: labelled metric bar, transcript/captions, inspected phone frame, desktop/phone playback; no accessibility user study. |
| Series progression | Meets design review: tests whether the collection and decision evidence from prior chapters can be maintained and accessed. |

## Completed checks

- Pronunciation-pack freshness and excerpt hashes; complete scene ASR inspected separately.
- Full FFmpeg decode, expected media streams, synchronized durations and five-second end card.
- Canonical caption text preserved, ordered and non-overlapping. Both four-second response holds have no active captions; exported audio silence checked with an AAC boundary margin.
- Actual encoded scene frames, response holds, staged reveals and phone rendering inspected.
- Chromium playback, seeking, captions, response holds, no overflow and linked map Example record at 960px and 390px; no page errors.
- Repeated packaging is idempotent: one page embed and manifest entry; previous chapters' provenance and original page prose preserved.
- Pronunciation unit tests, SQLite/example checks, map data/layout validation, full site build and `git diff --check` pass.

Working evidence remains in ignored `out/q1-chapter-08/`: raw speech and
provenance, original ASR, alignment, pronunciation clips, timings, captions,
encoded frames, media and browser reports. Publication is checked after merge.
