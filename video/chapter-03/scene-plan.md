# Chapter 3 page learning aid: follow the evidence behind 100%

Source: `chapters/03-following-lineage.md` and retained lineage SQL examples at
`c144d0f04f3d6f6737c812e4836b4e0c49266856`. Audience: report readers and engineers.
After watching, readers should follow matching identifiers from a report refresh
to its saved output and producing run, inspect its retained input/code, and
explain why the result was 100% without inferring that it remained current.

The approved Q1 original synthetic voice, book palette and coded figures are
retained. The page supplies complete lineage/provenance definitions and record
fields. The video demonstrates their use through one evidence trail. A persistent
four-step trail appears during investigation, with the current step highlighted.
Its arrows mean following references backwards, not the direction of data flow.

| Scene | Page source / learning task | Visual / timing | Interpretation guard |
|---|---|---|---|
| report-question | Opening and refresh record | 100% /13:00; ask whether refresh time establishes calculation time; four-second hold | Completed-delivery measure; invented incident; no answer during hold |
| route | Follow the route | Separate job→saved-result and saved-result→report actions | Refresh does not run calculation; do not substitute latest run |
| output | Which result did report read? | Match summary-R1205 on F1300 and output cards; reveal 55-minute gap and R1205 at speech cue | Publication 12:05 differs from refresh 13:00; identifier is evidence, not a timestamp parsed from its name |
| run-question | Which inputs/calculation? | R1205 branches to S1205 and completed-v1; ask if today's table suffices; four-second hold | References identify retained evidence; labels alone do not reproduce data/code |
| snapshot | Saved input S1205 | D101 11:50, D102 NULL, D103 11:40, D104 NULL; all promised noon | Complete retained 12:05 example, not the later input from Chapters 1–2 |
| calculation | Retained completed-v1 | Exclude D102/D104, retain D101/D103; reveal 2/2=100% at cue | Correct result for these inputs and this completed-only rule; no all-due substitution |
| meaning | Provenance / core points | Brief labels after demonstration; full definitions remain on page | Terms overlap; explaining 100% does not establish currency at refresh |
| practice | Existing reader action | Report refresh → Published output → Run → input/code | Explain first, then use page answer; map uses the same identifiers |
| end | Return / attribution | Five-second practice card | No new claim |

Exact authored narration is `narration.json`. Fresh independent unprompted ASR
supplies estimated word/sentence timing; no provider-boundary or listening claim.
Four-second `hold_seconds` values add silence after question speech and captions,
with the answer in the next scene. Review source meaning, recognition differences,
encoded frames and browser behaviour separately before packaging and merging.
