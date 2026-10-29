# Chapter 4: verify that recovery reaches the report

Source: `chapters/04-outdated-reports.md` and the lineage simulation at
`fac56101ce4f153f425d0150c302d1b5bb894910`. Audience: report readers and engineers.
Objective: explain stale output and identify both the new publication and the
report refresh that read it. Takeaway: a successful run alone is not proof of
report recovery. This embedded learning aid reinforces the page; detailed logs,
column-level lineage and the hypothetical wrong-filter example stay there.

Use approved Q1 narration and the book's cream/rust/green palette. No music.
Show actual identifiers and times as large excerpts. Forward publication/reading
arrows must not imply that a refresh executes the processing job.

| Scene | Source and visual action | Guard against misinterpretation |
|---|---|---|
| fresh-question | 13:00 report /100%, 12:20 late arrival; four-second prediction hold | No answer graphic during hold; completed-delivery measure |
| old-result | Two retained completed parcels /100 versus three current completed /66.7 | Same rule; 100 was correct for its older input; distinguish snapshots |
| failed-run | 12:30 R1230 failed before publication; then old output read at 13:00 | Injected permission fault is invented, not an instruction to change live permissions; failure alone does not identify displayed output |
| recovery-question | 13:10 publication /66.7%; ask if successful run alone proves report recovery; four-second hold | No later refresh shown yet; no further deliveries during recovery |
| recovery-answer | Match summary-R1310 on publication and F1312 /13:12 refresh; highlight link at speech cue | Need actual refresh reference, not simply temporal proximity or status=success |
| limits | Separate recovery and correct-logic checks; refer to page's separate hypothetical fault | Do not assert missing-filter fault caused this incident |
| retain | Earlier output + refresh + retained input/code | Historical explanation differs from reproduction; no deleted rows magically supplied by IDs |
| practice | Old map evidence versus page recovery table | New recovery records are not present in map; ask reader to use the page table |
| end | Five-second practice card, source credit and synthetic-voice disclosure | No new claim |

Narration is in `narration.json`; hold_seconds values add silence after question
speech/captions. Fresh independent unprompted ASR provides estimated alignment,
not provider boundaries or listening approval. Inspect excerpts, full transcripts,
actual encoded frames, caption text and paused-state browser behaviour separately.
Follow the explainer repository's Qwen and learning-aid guidance at `f16d0350df20cb35681886cb5d197ce27f2d3a49`.
