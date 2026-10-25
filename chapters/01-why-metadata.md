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

The disagreement comes from the denominator: the group against which we count successful deliveries. Choosing that group is a business decision. A correct calculation can still answer the wrong question for the person reading the report.

<blockquote class="key-principle" markdown="1">

**A metric's definition must say what counts.**

</blockquote>

## Record the decision

Suppose Delivery Operations wants to track whether all promised deliveries have arrived on time. A useful definition would record:

| Property | Recorded definition |
|---|---|
| Measure | Percentage of deliveries due that arrived on time |
| Counts as on time | Delivered at or before the promised time |
| Denominator | All deliveries due by noon, including those not yet delivered |
| Measured at | 13:00 UTC on the reporting date |
| Responsible team | Delivery Operations |
| Source | The `deliveries` table |

For our four parcels, this definition selects 50.0%. Another team could legitimately use the completed-delivery measure, provided its definition makes that choice clear.

The responsible team is the contact for questions about meaning. The account used to write a table does not tell readers which team to ask about its meaning. Likewise, a column named `delivered_at` does not establish which event counts as delivery. The definition needs to connect the system's fields to the business event people care about.

Keeping that decision beside the report saves each reader from reconstructing it. It also gives reviewers a way to recognise when two similarly named metrics should not be compared.

## Check the calculation against the definition

Recording a rule does not ensure that a query follows it. If the dashboard removes unfinished deliveries before counting, it will show 66.7% even though the recorded definition requires 50.0%.

The definition makes this disagreement testable. A reviewer can inspect the query's filters and denominator, then compare its output with the four-parcel example. If the intended rule changes, both the definition and the calculation need review.

A database already records some of the information that helps with this check: its table structure and saved query definitions. Those records are the starting point for the database example in Chapter 2.

<details class="further-detail" markdown="1">
<summary>Further detail: late updates and historical cutoffs</summary>

In a real system, an empty delivery time might mean an update has not arrived yet. A parcel delivered at 12:50 could be recorded at 13:10. Its event time and the time the system learned about it are different.

Reproducing what a report knew at 13:00 requires retained evidence, such as a timestamped snapshot or a change log. Reading the current table later may include information that was unavailable then. Chapter 3 uses captured inputs and execution records to investigate an older report.

</details>
