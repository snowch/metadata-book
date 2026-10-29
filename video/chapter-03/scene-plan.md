# Chapter 3 video contract and scene plan

Source: [Chapter 3](../../chapters/03-following-lineage.md), metadata-book commit `0fcdc702f0559c363876b5777b7034ea929a17b6`. Production method: the [authored video workflow](https://github.com/snowch/explainer-video-generator/blob/20ef33571f5b737c4fa267427964593836182205/docs/agent-video-workflow.md).

Audience: report readers and engineers. After watching, a reader should follow matching identifiers from a displayed number to the run, retained input and code that explain it. Approximately 3–4 minutes, one calm British narrator, cream/rust/green book palette. No music, dramatic hook or unrelated artwork. Exact narration lives in `narration.json`. Coded report and record diagrams explain relationships. This is an invented SQLite-backed example, not a production incident. It explains why 100% was calculated, without claiming it was current at the 13:00 refresh or introducing Chapter 4's recovery.

| Scene | Chapter source | Visual and timing | Interpretation guard |
|---|---|---|---|
| opening | Opening paragraph | Report display: 100%; completed-delivery measure; 13:00 UTC, 19 Oct 2026; invented example | Do not imply all four due parcels are the denominator. |
| route | Follow the route | Delivery records → scheduled job → saved output → report, with the report highlighted as its role is spoken | Arrows here mean data flow, not foreign keys. Refresh does not execute job. |
| distinction | Lineage and provenance | Complete definitions side by side, with the overlap and dependency-path limit stated beneath | Both can include transformations and actors; avoid how-versus-who simplification. |
| refresh | Which result did the report read? | F1300 card; highlight output_version summary-R1205 at the identifier cue | Refresh time does not establish result age. |
| output | Which result did the report read? | Matching output identifiers on two cards; show run R1205 and 12:05 publication; 55-minute interval | Inspection follows references backwards; state this direction explicitly in the scene subtitle. |
| run | Which inputs and calculation produced 100%? | Run R1205 → input S1205 and code completed-v1; reveal both references as spoken | References do not themselves preserve rows or SQL. |
| snapshot | Saved input S1205 | Four-row table; 11:50, NULL, 11:40, NULL; promised noon | Empty means unfinished only under complete-example assumption. This is the 12:05 input, not today's table. |
| calculation | Retained calculation | Exclude empty completion times; highlight D101/D103; 2/2 = 100% reveal | Do not substitute the later three-completed input; distinguish saved data from metadata references. |
| recap | Core points and Chapter 4 transition | Reference trail: refresh → output → run, branching to input/code | Arrows mean investigation, not processing order. Correct for retained input does not establish currency at refresh. |
| end | Attribution | Source chapter title and book link; synthetic-voice disclosure; five-second silent hold | No new claim or unverified copyright. |

Scene reveals and captions use fresh ASR alignment estimates to the canonical spoken text; unmatched words are explicitly flagged in the timing metadata. Manual source and visual review are separate from automatic transcription; no listening review is claimed. Display IDs stay exact while the pronunciation map makes them speakable.
