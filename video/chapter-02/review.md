# Chapter 2 page-learning-aid review — 29 October 2026

Replaces the full-chapter summary with a focused learning aid: predict what a
missing delivery time means, compare original and revised promises, predict
which parcel the saved query removes, then use the page's metadata-map exercise.
The full SQL, detailed schema fields, storage assumptions and catalogue
comparison remain on the page. Source: `2e8ef28ff22e9416377dba77a7819ab6e397e57f`.

## Actual export

2:18 (137.7 seconds), 1280×720, 24 fps, H.264/yuv420p, AAC and selectable English
captions. 38 caption cues; 3,677,228 bytes. Video SHA-256:
`e5a199d333e14961c0be6e1c9880703f1fa7f561a62058bbae731e0fb9548809`.
Seven complete Q1 narration passages; the original approved synthetic reference,
pinned Qwen Base checkpoint and unaltered speech tempo are retained. Six cached
passages survived interruption and passed content/model/hash checks; the missing
filter-question passage was regenerated from the same reference and settings.

## Learning and source review

Manually compared each scene and narration with the page and example SQL.
`delivered_at / TEXT / notnull:0` is a labelled column-record excerpt. The SQLite
type caveat is retained. NULL's alternative meanings are presented as
possibilities; unfinished is explicitly this complete example's convention.
The timeline distinguishes a noon promise from a revised 12:30 deadline for a
12:20 arrival without claiming when the revision occurred. The exact WHERE
clause is enlarged; the unfinished parcel is crossed out only after the
prediction scene. The late parcel remains in the completed group. The result
2/3=66.7% is distinguished from Delivery Operations' 2/4=50.0% rule. Fixed UTC
format and complete-record assumptions are spoken. The saved-query/output-data
distinction is preserved. The final exercise follows the page's Column, Saved
query and Metric definition records.

## Speech screening

Independent unprompted small.en ASR preserves the full-scene questions,
alternatives, negations and numbers. Estimated alignment coverage ranges from
98.1% to 100%; recognitions such as SQL light / SQL lite versus the intended
“sequel lite”, 1220/1230 versus spoken clock times, and “page is” versus “page's”
are retained in original ASR rather than rewritten as phonetic approval.
The pronunciation pack has 16 contextual clips and four recognition differences:
two SQLite spellings, NULL recognised as “no” in a short excerpt (the complete
scene recognises “null”), and 50.0% written as “50 percent”. The input-freshness
check passed before encoding. Complete passages were consulted where excerpts
cut surrounding words or introduced recogniser text.

**No human listening review was performed.** SQLite's exact phonetics and voice
expressiveness remain unresolved by recognition. No learner study or delayed
recall test is claimed; prediction pauses support practice by design.

## Completed checks

- Full FFmpeg decoding, expected media streams, video/audio duration agreement and five-second closing card.
- Captions concatenate exactly to canonical narration, in order without overlap.
- Both four-second response holds retain 4.693 and 4.508 seconds after the final caption; explanations appear in subsequent scenes.
- Inspected actual encoded frames for every scene, both holds and a 390-pixel rendering; the SQL filter, timeline and parcel relationship remain legible without displaying the full query.
- Chromium at 960px and 390px: playback, seeking, caption loading, no active captions during response holds, no page overflow and the metadata-map Example record activity.
- Existing pronunciation tests, SQL/example checks, map validation, layout consistency and full site build pass.

Working evidence is retained in ignored `out/q1-chapter-02/`: raw scene audio,
model metadata, independent ASR, alignment, pronunciation pack, captions,
timings, static previews, encoded contact sheet, phone frame, verification JSON
and browser screenshots. The production manifest retains scene provenance.
