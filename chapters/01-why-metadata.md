# 1. What the data cannot tell you

Consider a regional parcel delivery company taking a snapshot at 13:00 UTC on 19 October 2026. In this invented example, four deliveries were promised for noon. Three have a delivery time, one does not. A quick calculation says that two of the three completed deliveries arrived on time. That is 66.7 per cent. A different calculation says two of the four deliveries due arrived on time: 50.0 per cent.

Both calculations follow from the same rows. The choice between them depends on what the company means by “on-time delivery”. Is it measuring punctuality among parcels that have already been delivered, or the proportion of all due parcels that have been delivered on time by a stated point in the day? The table alone does not settle that question. To answer it, we need information about the data: what its fields mean, how it was produced, and how it should be used. That information is metadata.

## A small table, two answers

The snapshot contains these records. All timestamps are in UTC.

| Delivery ID | Promised at | Delivered at |
|---|---|---|
| D101 | 2026-10-19 12:00 | 2026-10-19 11:50 |
| D102 | 2026-10-19 12:00 | 2026-10-19 12:20 |
| D103 | 2026-10-19 12:00 | 2026-10-19 11:40 |
| D104 | 2026-10-19 12:00 | NULL |

For the first measure, exclude D104 because it has no delivery time. D101 and D103 were delivered before their promised times, while D102 was delivered afterwards. The result is 2/3, or 66.7 per cent, on time among completed deliveries.

For the second measure, count all four deliveries due that day. D104 had not been delivered by the 13:00 snapshot, so it had not met the promise by the cutoff. The result is 2/4, or 50.0 per cent, on time among deliveries due. Neither denominator is inherently correct. They answer different business questions, and a report should make clear which question it is intended to answer.

The values support these calculations only under some assumptions. “Promised at” must represent the applicable commitment for each parcel; “delivered at” must record the relevant delivery event; and a blank must mean that no qualifying delivery had occurred by the snapshot, rather than a missing or delayed update. A timestamp also needs a time zone or other clear convention. Here the snapshot explicitly supplies UTC, so there is no need to guess how to compare the times.

## Metadata describes data in context

Metadata is information describing data: its meaning, structure, and how it is produced or managed. The label is relational. A column name such as `delivered_at` is metadata about a field; a table schema is metadata about a table; and a catalogue entry describing that schema is metadata about the catalogue object. The same item can be data in one context and metadata in another.

Metadata does not have to live in a separate catalogue or document. A column name, a database constraint, a timestamp stored alongside an event, a transformation definition, and a steward’s written metric definition can all carry metadata. Some of it is formal and machine-readable; some exists in operational procedures or in the knowledge of the people who maintain a system. Keeping it discoverable matters, because otherwise people infer meaning from names, values, and local custom.

The rows show values and a rough shape: one identifier and two timestamps per delivery. They do not explain whether the promise is the original estimate or the latest customer commitment, whether “delivered” means handed to the recipient or left at a safe place, or when a parcel counts as due. A familiar column name can conceal these choices. Two systems can both have a `delivered_at` field and use it for different events.

## Record the decision behind a metric

A short definition makes the intended calculation inspectable. For this example, a metric record could be:

| Property | Definition |
|---|---|
| Metric | On-time among deliveries due |
| Business definition | Deliveries due on the reporting date with a qualifying delivery at or before the promised time, divided by all deliveries due on that date |
| Denominator | All deliveries due on the reporting date, including those not yet delivered |
| Cutoff | Snapshot taken at 13:00 UTC on 2026-10-19 |
| Owner | Delivery Operations |
| Source | `deliveries` |

The record makes the denominator explicit and fixes the evaluation time. The owner is the responsible team for the business meaning and its use. It is not necessarily the database account that reads or writes the table. The source points to the table that supplies the records, while a fuller definition would identify the relevant columns and the rule for interpreting null values.

Recording this definition resolves ambiguity for readers of the metric: the 50.0 per cent figure is the one that matches this stated denominator and cutoff. It does not prove that a dashboard or query implements the definition. A query might drop null delivery times before counting the denominator, use a different cutoff, or join to a source that has duplicate rows. The metadata gives implementers and reviewers something concrete to compare with the calculation; data quality checks and inspection of the implementation are still needed.

## Structure is not the same as meaning

A database schema describes structural properties that a database can enforce or expose: table and column names, data types, nullability, keys, and relationships. For example, the schema might say that `promised_at` and `delivered_at` are timestamps and that `delivery_id` is a key. Those facts help software read and validate the table. They do not fully define the business events those columns represent.

Meaning usually spans more than the schema. A type of timestamp cannot tell us which promise applies after a customer reschedules, what counts as a completed delivery, or whether a late-arriving update changes a previously reported result. Those rules may be captured in data contracts, metric definitions, transformation logic, or operational policy. Each is metadata when it describes the data or how it is handled, even if stored in a different place.

It is useful to keep the layers connected. A metric definition can name a source table and its fields; the schema can provide the physical names and types; and the production process can explain where the values originate. If one of these changes, a definition may need review. Renaming a column is a structural change. Changing which delivery event populates it is a change in meaning, even if the column name and type remain untouched.

## A snapshot is not a history

At 13:00, D104 has a null delivery time in the supplied snapshot. That tells us the value recorded in that snapshot, subject to the source’s update behaviour. It does not by itself tell us whether D104 was delivered at 13:05, whether an earlier update was corrected, or whether the row was absent from a previous extract. A current table can describe current records while losing the evidence needed to reconstruct what was known earlier.

Historical questions need historical evidence: for example, timestamped snapshots, an append-only event log, or an audit trail that records changes. Such records can show when an event occurred and when the system learned of it, which are not always the same time. The 13:00 cutoff in the metric definition is therefore meaningful only if the source or its retained snapshots let the company reproduce what it knew at that cutoff.

The database already holds some of the information we need: its table structure and any saved queries that calculate the metric. Inspecting those records lets us compare the implemented calculation with the business definition.
