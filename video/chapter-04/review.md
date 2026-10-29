# Chapter 4 learning-aid review — 29 October 2026

Objective: explain stale output and identify the publication plus report refresh
that establish recovery. Source: `fac56101ce4f153f425d0150c302d1b5bb894910`.
Guidance: explainer repository `f16d0350df20cb35681886cb5d197ce27f2d3a49`.

## Export and speech

2:32 (152.2 seconds), 1280×720, 24 fps, H.264/yuv420p, AAC and selectable English
captions. 43 caption cues, 4,096,088 bytes. SHA-256:
`a7253d07403df9b9f7de3386161a44e9e4274c55349f5ce8d86bb543423c8d65`.
Eight new complete passages use the approved original synthetic Q1 reference and
pinned Qwen Base checkpoint. No tempo alteration or generated-word trimming.

Independent unprompted small.en ASR preserves percentages, identifiers, times,
negations, deliberate-fault context and the separate hypothetical logic fault.
Estimated alignment coverage is 100% except the recovery answer (99.2%), where
“too”/“to” and past-tense “read”/“red” differ in recognition spelling. Original
ASR remains separate from canonical timing. The pronunciation pack has 20 clips
and one term-spelling difference: summary-R1310 becomes “summary are 1310” in a
short excerpt; the full passage retains the intended identifier. Some short
excerpts cut context or add recognition text. In particular, full-scene ASR
preserves “No further deliveries” despite an excerpt beginning later in that
sentence. The freshness/hash check passed before encoding.

**No human listening review was performed.** Exact phonetics, accent and voice
expressiveness remain screened rather than listening-approved. Reference-voice
approval does not establish listening approval of these new passages.

## Learning-aid rubric

| Criterion | Finding / evidence |
| --- | --- |
| Alignment and relevance | Meets design review: all scenes trace the page's stale-output/recovery incident; detailed logs and column-level debugging stay on the page |
| Clarity | Design review: the two questions have explicit later explanations; reader understanding is not assessed |
| Visual explanation | Meets design review: retained/current ratios and matching publication/refresh references explain two different checks |
| Focus and memorability | Meets design review: one anchor, publication AND actual report read; delayed recall is not assessed |
| Active recall | Meets export review: questions at 0:00 and 0:55.67 retain four-second silent holds before answer scenes |
| Application and page connection | Meets browser review: map earlier records are compared with the page's recovery table; transfer to a different incident is not assessed |
| Cognitive load and pacing | Meets design review: large record excerpts and one relationship per scene; full debugging evidence remains on the page |
| Engagement | Design judgment: a current-result question leads through failure to verified recovery; no viewer engagement study |
| Accuracy | Meets source review: same rule, changed input; injected permission failure; separate wrong-logic example; no further arrivals during recovery; retained data/code needed for reproduction |
| Accessibility and control | Meets tested scope: labels supplement colour, transcript/captions, encoded phone frame and 960px/390px playback checks; no user accessibility study |
| Series progression | Meets source review: continues Chapter 3's saved 100% without calling it incorrect for its inputs; prepares for collecting records from different systems |

The map intentionally shows the earlier F1300/summary-R1205 evidence. It does not
contain recovery examples. The video explicitly asks readers to use the page's
recovery table for F1312/summary-R1310; a failed status alone does not establish
what readers saw, and a successful run alone does not establish report recovery.

## Completed verification

- Full FFmpeg decode; expected streams, matching audio/video durations, five-second closing card.
- Exact canonical caption text, ordered/non-overlapping cues; response holds leave 4.573 and 4.654 seconds after final captions.
- Inspected actual encoded frames from every scene and both holds, plus phone-size rendering; no answer reveal during a question hold.
- Chromium at 960px and 390px: playback, seeking, captions, no active caption in holds, no overflow, and map Example record activity.
- New-chapter packaging rerun is idempotent: one embed and one manifest record; Chapters 1–3 provenance is unchanged; original Chapter 4 prose is preserved outside the embed.
- Existing pronunciation tests, SQLite/example checks, map validation, layout consistency and full site build pass.

Evidence is retained in ignored `out/q1-chapter-04/`: raw audio/provenance, ASR,
word alignment, pronunciation pack, timings, captions, encoded frames/contact
sheet, phone frame, media and browser verification reports and screenshots.
Reader retention/transfer outcomes remain not assessed.
