# Chapter 1 learning aid: choose the denominator, then check the rule

Source: `chapters/01-why-metadata.md` at `476c510abafeb8fc94a847b43595d3ae0d21e487`.
Purpose: reinforce the page, rather than repeat its reference material. Audience:
report readers and engineers. After watching, readers should explain why the
unfinished parcel changes the denominator, distinguish a recorded definition
from its implementation, and complete the page's metadata-map exercise.

Use the approved original synthetic Q1 voice, cream/rust/green palette, coded
parcel drawings and large labels. No music. The page carries the full metadata
definition, complete metric record and field-name discussion. Do not imply the
video replaces those details. Narration is authored in `narration.json`.

| Scene | Source idea | Visual / learning action | Interpretation guard |
|---|---|---|---|
| puzzle | Two ways to count deliveries | Two percentages, one question | Neither percentage is universally wrong |
| parcels | Invented complete four-parcel example at 13:00 | Same four labelled parcels used throughout | Noon is the promised deadline, not the measurement time |
| predict | Completed-delivery denominator | Choose 2, 3 or 4; four-second response hold | No answer is shown before the hold ends |
| completed | Two on time / three completed | Include the late parcel; bracket first three; reveal 66.7% at speech cue | Late is completed; unfinished remains visible outside group |
| due | Two on time / all four due | Expand bracket to fourth parcel at speech cue; reveal 50.0% | Numerator stays two; the question changes |
| rule | Record the decision | Three focused excerpts: inclusion, measurement time, responsible team | Label as excerpts; complete record stays on page; recorded time is 13:00 UTC on reporting date |
| challenge | Check calculation against definition | All-due rule versus 66.7%, successful query; five-second response hold | Do not reveal explanation during retrieval pause |
| answer | Query excludes unfinished | Show rule denominator four and query denominator three; compare results | Mismatch is relative to Delivery Operations' all-due rule |
| practice | Existing metadata-map reader action | Metric definition → Example record; explain before revealing page answer | Responsibility explains meaning, not proof of execution correctness |
| end | Attribution / return to page | Five-second silent practice card | No new claims |

New speech uses pinned Qwen Base and exact Q1 reference. Independent unprompted
ASR supplies estimated sentence/word timing. `hold_seconds` adds deliberate
silence after the complete question, before the answer scene; it does not slow
speech or extend captions over silent thinking time. All labels and cues are
checked against the page manually. Automated recognition is screening, not a
listening review or proof of educational effectiveness.
