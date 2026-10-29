# Chapter 11 learning-aid review — 29 October 2026

Source: `cca707e3c3bdd295aa85becf94984d3e4b6fa20a`. Guidance: explainer
`f16d0350df20cb35681886cb5d197ce27f2d3a49`. Audience: report readers and
engineers. Objective: Distinguish recorded access approval from enforced controls, and a planned synthetic release from permission to share operational records.

Free workspace disk space before starting: 25 GB available (20% used). Checked with `df -h /workspace`.

## Export and speech

2:40 (160.300 seconds), 1280×720 at 24 fps, H.264/yuv420p,
AAC and selectable English captions. 43 cues; 4,414,404 bytes.
SHA-256: `365ec1fb4f8884e7911baae96a51d3722deeb25f69fdce6e863efb6620973bb9`.

Approved original synthetic Q1 reference and pinned Qwen Base model. Complete
passages retained without generated-word trimming or tempo alteration. Original
independent, unprompted small.en ASR is separate from canonical text and estimated
alignment. Matched-character coverage 97.7–100.0%.
Pronunciation pack: 11 contextual excerpts, 1
text mismatches. Full-scene ASR preserves purpose/control distinctions, the proposed CC BY 4.0 synthetic release, the complete FAIR expansion and deletion/rerun limits. Differences are catalogue/catalog, authorise/authorize and CC letter spelling against the pronunciation expansion. Of 11 term excerpts, one mismatch is catalogue/catalog. The practice passage matches the actual Access decision card; the other five valid audio passages were retained with their original hashes and batch provenance. Original ASR remains separate; no phonetic or listening approval is inferred.

**No human listening review was performed.** Recognition screens words and
identifiers; it does not certify phonetics, accent, naturalness or delivery.
Reader understanding, engagement, delayed recall and transfer outcomes are
**not assessed**; the rubric below records design/source/export judgments.

## Learning-aid rubric

| Criterion | Finding and evidence |
|---|---|
| Alignment and relevance | Meets source/design review: explicit purpose, enforced controls, separate synthetic publication and retention limits. |
| Clarity | Design review: access-label and planned-release questions receive later explicit answers; reader understanding unassessed. |
| Visual explanation | Meets encoded-frame review: decision/implementation/test path, separate operational/synthetic identities and later FAIR expansion. |
| Focus and memorability | Design review: keep purpose, identity and actual status explicit; delayed recall unassessed. |
| Active recall | Meets export review: two four-second silent holds; enforcement and operational-export verdicts appear in later answer scenes. |
| Application and page connection | Meets tested scope: Access decision → Reuse description; compare purpose, version, pending ID and proposed license, then page feedback. |
| Cognitive load and pacing | Design review: short control/status excerpts; full retention periods and repository requirements stay on page. |
| Engagement | Design judgment: practical access and reuse decisions give a reason to inspect identities and evidence; viewer engagement unassessed. |
| Accuracy | Meets source review: label not enforcement, unrelated purpose needs decision, revocation not recall, wholly synthetic planned dataset distinct, FAIR not permission/public requirement, deletion limits preserved. |
| Accessibility and control | Meets tested scope: explicit labels supplement colour, transcript/captions, inspected phone frame, desktop/phone playback; no accessibility user study. |
| Series progression | Meets design review: closes the series by applying meaning, evidence and version lessons to controlled access and reuse without authorising operational release. |

## Completed checks

- Pronunciation-pack freshness and excerpt hashes; complete scene ASR inspected separately.
- Full FFmpeg decode, expected media streams, synchronized durations and five-second end card.
- Canonical caption text preserved, ordered and non-overlapping. Both four-second response holds have no active captions; exported audio silence checked with an AAC boundary margin.
- Actual encoded scene frames, response holds, staged reveals and phone rendering inspected.
- Chromium playback, seeking, captions, response holds, no overflow and linked map Example record at 960px and 390px; no page errors.
- Repeated packaging is idempotent: one page embed and manifest entry; previous chapters' provenance and original page prose preserved.
- Pronunciation unit tests, SQLite/example checks, map data/layout validation, full site build and `git diff --check` pass.

Working evidence remains in ignored `out/q1-chapter-11/`: raw speech and
provenance, original ASR, alignment, pronunciation clips, timings, captions,
encoded frames, media and browser reports. Publication is checked after merge.
