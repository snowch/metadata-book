# Chapter 10 learning-aid review — 29 October 2026

Source: `8c49ce03dfb8bab5317318d40eb6a687091edc8e`. Guidance: explainer
`f16d0350df20cb35681886cb5d197ce27f2d3a49`. Audience: report readers and
engineers. Objective: Explain semantic incompatibility despite an unchanged schema, and distinguish an approved design from evidence-backed release.

Free workspace disk space before starting: 25 GB available (19% used). Checked with `df -h /workspace`.

## Export and speech

2:32 (152.200 seconds), 1280×720 at 24 fps, H.264/yuv420p,
AAC and selectable English captions. 40 cues; 4,180,454 bytes.
SHA-256: `fcbd3ca3df09ab879b8512286edb11a08bdffb6a289a34cd22198ed3699fcd4f`.

Approved original synthetic Q1 reference and pinned Qwen Base model. Complete
passages retained without generated-word trimming or tempo alteration. Original
independent, unprompted small.en ASR is separate from canonical text and estimated
alignment. Matched-character coverage 98.7–100.0%.
Pronunciation pack: 12 contextual excerpts, 2
text mismatches. Full-scene ASR preserves the 12:20 versus noon/12:30 distinction, November dates, pending release, required consumer/producer evidence and history. Differences include approve/approved, planned/plan, read/red, ordinal date formatting and promised at/it in the practice scene. Of 12 term excerpts, two text mismatches concern deliveries version one/1 and promised at/it. Full context was inspected; exact pronunciation and expressive delivery remain unassessed without listening.

**No human listening review was performed.** Recognition screens words and
identifiers; it does not certify phonetics, accent, naturalness or delivery.
Reader understanding, engagement, delayed recall and transfer outcomes are
**not assessed**; the rubric below records design/source/export judgments.

## Learning-aid rubric

| Criterion | Finding and evidence |
|---|---|
| Alignment and relevance | Meets source/design review: semantic change, consumer agreement and release evidence are separated. |
| Clarity | Design review: classification/denominator and approval/release questions receive later explicit answers. |
| Visual explanation | Meets encoded-frame review: same arrival compared against two promises; denominator membership revealed later; approval and release requirements distinct. |
| Focus and memorability | Design review: unchanged schema does not preserve meaning; approval alone is not release; delayed recall unassessed. |
| Active recall | Meets export review: two four-second silent holds before explicit classification/membership and release answers. |
| Application and page connection | Meets tested scope: Data contract deliveries-v1 meaning/change rule, then page feedback. |
| Cognitive load and pacing | Design review: short field/date excerpts; complete revised-field definition, contract versions and evidence requirements remain on page. |
| Engagement | Design judgment: concrete promise change and conditional release decisions invite reasoning; viewer engagement unassessed. |
| Accuracy | Meets source review: hypothetical scenario labelled, 12:20 comparisons correct, absent-revision choice retained, approved design pending release, roles/history/restatement preserved. |
| Accessibility and control | Meets tested scope: time and classification labels supplement colour, transcript/captions, inspected phone frame and desktop/phone playback; no accessibility user study. |
| Series progression | Meets design review: develops earlier promise-change proposal without altering the source fixture or incident history. |

## Completed checks

- Pronunciation-pack freshness and excerpt hashes; complete scene ASR inspected separately.
- Full FFmpeg decode, expected media streams, synchronized durations and five-second end card.
- Canonical caption text preserved, ordered and non-overlapping. Both four-second response holds have no active captions; exported audio silence checked with an AAC boundary margin.
- Actual encoded scene frames, response holds, staged reveals and phone rendering inspected.
- Chromium playback, seeking, captions, response holds, no overflow and linked map Example record at 960px and 390px; no page errors.
- Repeated packaging is idempotent: one page embed and manifest entry; previous chapters' provenance and original page prose preserved.
- Pronunciation unit tests, SQLite/example checks, map data/layout validation, full site build and `git diff --check` pass.

Working evidence remains in ignored `out/q1-chapter-10/`: raw speech and
provenance, original ASR, alignment, pronunciation clips, timings, captions,
encoded frames, media and browser reports. Publication is checked after merge.
