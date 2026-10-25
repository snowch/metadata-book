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

Finding a definition is not the same as finding a working report. Delivery Operations confirms the intended population; the reporting engineer checks that the proposed calculation includes unfinished parcels and reproduces 50.0%. If no existing calculation passes that check, the next action is to implement and review one. A search result should not conceal that gap.

## Separate quality checks from meaning

Suppose checks find no duplicate delivery identifiers and confirm that all four promised times are present. Those results support specific claims about the checked records. They do not establish that a completed-delivery measure answers the all-due question. A fresh, correctly calculated 66.7% would still answer a different question.

The reverse also matters. A definition can match the request while its report displays an old output. In Chapter 3, the 13:00 refresh read `summary-R1205` after the 12:30 run failed. The reporting engineer must inspect the publication and refresh records before presenting that value as current.

Record which data version a check covered and when it ran. A successful check on yesterday's output says little about today's publication. An empty `delivered_at` is also allowed in this example: treating every missing delivery time as a defect would reject a legitimate unfinished parcel.

<blockquote class="key-principle" markdown="1">

**Match each decision to evidence that can support it, and state what remains unknown.**

</blockquote>

## Scope a proposed change

Suppose `promised_at` currently records the original customer promise. A proposed change would use the latest revised promise instead. A parcel arriving at 12:20 is late against a noon promise but on time against a revised 12:30 promise. The column's name and type would not reveal this change. Both teams need to review how it affects their measures before the reporting engineer changes the source.

The collected dependency path identifies `build_delivery_summary`, `delivery_summary` and Delivery performance for review. The engineer checks those consumers' definitions, tests representative parcels against both promise rules, and arranges a report update with its owner.

That path establishes a review scope only within the collected evidence. An observed read proves that a consumer used the source during the recorded period. No observed read does not prove that a monthly report, an uncollected database or a downloaded spreadsheet is unaffected. State the covered systems and dates, ask the source owner about known gaps, and keep unresolved consumers on the change record.

## Leave a decision someone can act on

For the meeting, record: Delivery Operations requires the all-due rule; the reporting engineer will verify the four-parcel result and the published version before supplying it. For the promise change, record the affected consumers found, coverage gaps and who must review them. Metadata has done useful work when another person can see the evidence, the remaining uncertainty and the next action.
