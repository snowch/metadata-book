# Chapter 2 scene plan

Source: `chapters/02-reading-a-database.md` and `examples/deliveries.sql`, pinned in `project.json`. Invented four-row snapshot; no customer data. Target approximately 3–4 minutes, 500 narration words, original synthetic Q1 British female voice, no music. Cream, rust and green match existing chapter videos.

| Scene | Source and purpose | Visual treatment |
|---|---|---|
| opening | Opening: database descriptions are queryable | Database/table illustration with three structural facts; example disclosure |
| columns | Inspect the columns; actual pragma result | Exact query above readable three-row table: name, type, notnull, pk. All TEXT; flags 1/1, 1/0, 0/0. Small legend explains declared type, required value, key position; narration states SQLite type caveat |
| meaning | Structure versus meaning; missing delivery time | Three possible interpretations of a missing delivery time (no causal arrows); clearly mark unfinished as this example's convention |
| promise | Original versus revised promise | Timeline with noon, 12:20 arrival and 12:30 revised promised deadline; label arrival late for original and on time for revised. Make comparison simultaneous and explicit |
| view | Read the calculation | Entire CREATE VIEW definition copied verbatim from `examples/deliveries.sql` lines 15–25; visible at 24px monospaced type across all 11 lines; highlight WHERE line after filter cue. Explain view recalculates when read; zero-denominator guard returns NULL |
| count | Completed population versus all due | Actual rows D101 11:50, D102 12:20, D103 11:40, D104 NULL; all promises noon. Two side-by-side result cards: 2/3 completed = 66.7%, 2/4 all due = 50.0% |
| assumptions | Fixed UTC text and saved-query/output distinction | Exact timestamp format with sample; calculation metadata card leading to output-data card. Explicit format assumption, not TEXT guarantee |
| catalogues | Two jobs for a catalogue | Two columns: software / Hive Metastore with schema, partition, location, format; people / DataHub + OpenMetadata with definition, responsibility, lineage. Shared overlap band for comments and ownership |
| recap | Core points | Structure → meaning → calculation, with three concrete questions; no Chapter 3 incident identifiers |
| end | Source and disclosure | Title, book URL, attribution, invented example and synthetic narration |

Narration avoids reading SQL identifiers as prose. Captions preserve the display narration; the pronunciation lexicon changes speech only. SQLite is “sequel lite”; 66.7% is “sixty six point seven percent”; 50.0% is “fifty percent”. Review the complete script before synthesis. Generate and review the shared pronunciation audit after synthesis and before rendering. Record the pronunciation review method and any unresolved concerns before encoding.

SQL source trace: the column-inspection statement is from the chapter’s “Inspect the columns” block; the displayed 11-line view is copied verbatim from `examples/deliveries.sql` (`CREATE VIEW` through `WHERE delivered_at IS NOT NULL;`). The actual four rows are copied from that file’s INSERT statement. The promise timeline labels 12:30 as a revised promised delivery deadline; it does not assert when that revision occurred.
