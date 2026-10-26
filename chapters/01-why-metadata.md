# 1. What the data cannot tell you

A dashboard shows a number. To use it, we need to know what it measures, where it came from, and how it was calculated. The values alone rarely supply those answers.

**Metadata is information that describes data:** its structure, meaning, origin and use. Column names and types are metadata. So are a metric's definition and a record of the job that produced it. These descriptions may live inside a database, alongside a report, or in a separate catalogue.

## What a number means

Even a familiar label such as “on-time delivery” leaves room for different calculations.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Two ways to count deliveries</figcaption>

A parcel company promised four deliveries by noon. At 13:00, two have arrived on time, one arrived late, and one has not arrived. This is an invented example; assume the delivery records are complete at that moment.

| Question | Calculation | Result |
|---|---|---:|
| Of the **completed deliveries**, how many were on time? | 2 out of **3** | 66.7% |
| Of **all deliveries due**, how many arrived on time? | 2 out of **4** | 50.0% |

Both calculations are valid for their stated questions. The first measures punctuality among completed deliveries. The second also counts the parcel still waiting to arrive. A dashboard labelled only “on-time delivery” leaves its readers to guess which question it answers.

</figure>

The disagreement comes from the denominator: the total number of deliveries included—three completed deliveries or all four deliveries due. Choosing that group is a business decision. A correct calculation can still answer the wrong question for the person reading the report.

## Record the decision

Suppose Delivery Operations uses the second definition: of all deliveries promised by noon, what proportion arrived on time? A useful definition would record:

| Property | Recorded definition |
|---|---|
| Measure | Percentage of deliveries due that arrived on time |
| Counts as on time | Delivered at or before the promised time |
| Denominator | All deliveries due by noon, including those not yet delivered |
| Measured at | 13:00 UTC on the reporting date |
| Responsible team | Delivery Operations |
| Source | The `deliveries` table |

For our four parcels, using this definition gives 50.0%. Another team could legitimately use the completed-delivery measure, provided its definition makes that choice clear.

The definition should name the team that can explain what the metric means—for example, Delivery Operations.

Column names also need explanation. Does `delivered_at` record when a parcel reached a depot or when it reached the customer? Both are plausible meanings; the name alone cannot tell us which one applies.

A recorded definition helps readers understand what a number measures. It also reveals when similarly named metrics count different things and should not be compared directly.

*Later in the book, [Chapter 7](07-choosing-a-platform.md) compares ways to store and maintain these definitions, from reviewed documents to a metadata catalogue.*

## Check the calculation against the definition

Recording a rule does not ensure that a query follows it. If the dashboard removes unfinished deliveries before counting, it will show 66.7% even though the recorded definition requires 50.0%.

The definition makes this disagreement testable. A reviewer can inspect the query's filters and denominator, then compare its output with the four-parcel example. If the intended rule changes, both the definition and the calculation need review.

A database already records some of the information that helps with this check: its table structure and saved query definitions. Those records are the starting point for the database example in Chapter 2.

## Core points

- **A metric must say what counts.** Completed deliveries and all deliveries due answer different questions, even when both are labelled “on-time delivery.”
- **Record the definition and responsible team.** Readers need to know what is included, when it is measured and whom to ask about its meaning.
- **A definition is something to check against.** Inspect the calculation to verify that its filters and denominator follow the recorded rule.

<details class="further-detail" markdown="1">
<summary>Further detail: late updates and historical cutoffs</summary>

In a real system, an empty delivery time might mean an update has not arrived yet. A parcel delivered at 12:50 could be recorded at 13:10. Its event time and the time the system learned about it are different.

Reproducing what a report knew at 13:00 requires retained evidence, such as a timestamped snapshot or a change log. Reading the current table later may include information that was unavailable then. Chapter 3 uses captured inputs and execution records to investigate an older report.

</details>
