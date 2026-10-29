# Chapter 2 page learning aid: structure, meaning, calculation

Source: `chapters/02-reading-a-database.md` and `examples/deliveries.sql` at
`2e8ef28ff22e9416377dba77a7819ab6e397e57f`. Audience: report readers and engineers.
Afterwards readers should explain the limits of a column record, predict which
row the saved query removes, and compare its denominator with the definition.

The approved original synthetic Q1 voice and book palette continue. Use large
column excerpts, a promise timeline, four recurring parcels and one enlarged
SQL filter. The full SQL, detailed type/key explanation, timestamp assumptions
and catalogue comparison remain on the page. This is reinforcement, not a
complete substitute for reading the chapter.

| Scene | Page source / purpose | Visual and learning action | Interpretation guard |
|---|---|---|---|
| schema | Inspect the columns | Exact delivered_at / TEXT / notnull:0 excerpt; predict NULL meaning; four-second hold | Explicit SQLite type caveat; permit NULL does not explain it |
| meaning | Missing time alternatives | Three possible meanings; reveal this example's complete-record convention at speech cue | Do not assert unfinished is the universal meaning of NULL |
| promise | Original/revised promise | Noon, 12:20 arrival, 12:30 revised promise; two speech-timed verdicts | Revised deadline is not the time the promise was changed |
| filter-question | Read the calculation | Exact WHERE clause excerpt, four parcels and NULL on the unfinished one; four-second hold | No crossed-out parcel or percentage before response hold ends; SQLite view recalculates when read |
| filter-result | Filter and actual output | Cross out unfinished only; retain late parcel; reveal 2/3=66.7% at speech cue | Complete-record and fixed UTC text-format assumptions spoken |
| compare | Calculation vs business rule | Three completed /66.7 versus four due /50; query metadata versus returned output data | Metadata does not itself choose the business rule |
| practice | Existing reader action | Column → Example record; Saved query vs Metric definition | Require explanation before using page answer |
| end | Return and credit | Five-second practice card | No new factual claim |

Narration is authoritative in `narration.json`. Sentence cues use independent
unprompted ASR alignment estimates, not provider boundaries. `hold_seconds`
adds silence after each question. Review all ASR, pronunciation excerpts and
actual encoded frames. Record automated screening separately from listening.
