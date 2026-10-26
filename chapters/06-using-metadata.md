# 6. Using metadata to make decisions

Metadata helps someone choose a dataset, decide whether to use a result, or prepare a change. Each decision needs different evidence. A definition explains what a measure counts; a test result describes a particular check; a dependency record points to a possible consumer. Useful decisions keep those differences visible.

## Find the measure that answers the question

Delivery Operations asks: “Of all parcels due by noon, how many arrived on time?” Searching for “on-time delivery” finds the `on_time_completed` view and Service Analytics' Delivery performance report. Familiar names make both plausible candidates. Their definitions and calculations determine whether either answers the question.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Choosing a measure for the operations meeting</figcaption>

Use the four parcels from Chapter 1, with the same complete records at 13:00.

| Candidate | What it tells us |
|---|---|
| Completed-delivery view | Excludes parcels without a delivery time and returns 66.7%. It answers a different question. |
| Delivery performance report | Also uses the completed-delivery rule. Refreshing it would not make it suitable for this meeting. |
| Agreed all-due definition | Includes all four parcels due; two arrived on time, giving 50.0%. This is the right rule, but we still need a verified calculation. |

</figure>

Finding a definition is not the same as finding a working report. Delivery Operations confirms which parcels the measure must include; the reporting engineer checks that the proposed calculation includes unfinished parcels and reproduces 50.0%. If no existing calculation passes that check, the next action is to implement and review one. The catalogue should make clear that the agreed definition still needs a working calculation.

## Separate quality checks from meaning

Suppose checks find no duplicate delivery identifiers and confirm that all four promised times are present. Those results support specific claims about the checked records. They do not establish that a completed-delivery measure answers the all-due question. A fresh, correctly calculated 66.7% would still answer a different question.

The reverse also matters. A definition can match the request while its report displays an old output. In Chapter 3, the 13:00 refresh read `summary-R1205` after the 12:30 run failed. The reporting engineer must inspect the publication and refresh records before presenting that value as current.

Record which data version a check covered and when it ran. A successful check on yesterday's output says little about today's publication. An empty `delivered_at` is also allowed in this example: treating every missing delivery time as a defect would reject a legitimate unfinished parcel.

## Scope a proposed change

Suppose `promised_at` currently records the original customer promise. A proposed change would use the latest revised promise instead. A parcel arriving at 12:20 is late against a noon promise but on time against a revised 12:30 promise. The column's name and type would not reveal this change. Both teams need to review how it affects their measures before the reporting engineer changes the source.

The dependency path points to `build_delivery_summary`, `delivery_summary` and Delivery performance. The engineer checks how the change would affect each one, compares results under both promise rules, and agrees any report changes with its owner.

This path identifies places to check, but collection may have missed others. A recorded read shows that a job or report used the source at that time. A monthly report or downloaded spreadsheet may be missing from those records. Record which systems and dates were checked, ask the source owner about gaps, and list any uses of `promised_at` that still need investigation.

## Leave a decision someone can act on

For the meeting, record: Delivery Operations requires the all-due rule; the reporting engineer will verify the four-parcel result and the published version before supplying it. For the promise change, record the affected jobs and reports, any gaps in the investigation and who will check them. Metadata has done useful work when another person can see the evidence, the remaining uncertainty and the next action.

## Core points

- **Choose data by the question it answers.** A familiar name does not establish that a measure uses the required definition.
- **Quality checks support specific claims.** Passing checks does not prove that a measure answers the business question or that a report is current.
- **Dependencies identify places to investigate.** They do not prove that every affected report or spreadsheet has been found.
- **Leave an actionable decision.** Record the evidence, remaining uncertainty, next action and who will take it.
