# 3. Following a number to its source

To explain a number in a report, we need to know both the route from its sources and what happened when that result was produced.

<div class="definition-box" markdown="1">

**Lineage**

Records where data comes from, how it is transformed, and which datasets or reports depend on it.

</div>

<div class="definition-box" id="provenance" markdown="1">

**Provenance**

Records the history of a particular dataset or result: who or what created or changed it, when, and using which sources and methods.

</div>

Lineage emphasises **data flow**; provenance emphasises **creation and change history**. Both can describe transformations and the people or systems involved, so the distinction is not simply “how” versus “who.” The terms overlap in practice; lineage tools can also capture provenance.

Knowing which table and calculation a report normally uses is only part of the explanation. To explain a displayed number, we need to know which run produced it, which input data it read, and which version of the processing code it executed.

## Follow the route

Another department, Service Analytics, measures the percentage of **completed deliveries that arrived on time**. It excludes parcels still awaiting delivery. The `on_time_completed` view calculates this percentage whenever it is read.

Now suppose a scheduled job, `build_delivery_summary`, uses that same calculation to write a stored table called `delivery_summary`. Publishing a new result makes it available to reports. If a run fails before publishing, reports can still read the previous result.

<figure class="lineage-diagram" aria-labelledby="lineage-caption">
<figcaption id="lineage-caption">Declared dependency path</figcaption>
<ol>
<li><span class="flow-role">Source table</span><code>deliveries</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Scheduled job</span><code>build_<wbr>delivery_<wbr>summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Stored result</span><code>delivery_summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Report</span>Delivery performance</li>
</ol>
</figure>

The route identifies the job to investigate. It does not tell us which execution supplied the report's current number.

## Start with the version the report read

At 13:00 on 19 October 2026, Delivery performance shows **100%**. Running the completed-delivery calculation against the current source gives **66.7%**. Both use the same rule. We need to find out whether they used the same inputs and code.

This is an invented incident. A [small SQLite simulation](../examples/lineage/README.md) creates the records and computes the results shown here. Its clock times and failure are scripted; it is not a trace captured from a live reporting system. All times in this investigation are UTC on 19 October.

Start with the report's own refresh record. Looking only at the latest successful job could lead us to a result the report never read.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · The report's refresh record</figcaption>

| Field | Recorded value |
|---|---|
| Refresh | `F1300` |
| Report | Delivery performance |
| Refreshed at | 13:00 |
| Output read | `summary-R1205` |

</figure>

The simulation stores this in `report_refreshes`. The output identifier names a specific saved result, whose percentage is 100%. The simulation represents `delivery_summary` using saved rows in `outputs` and a `current_output` reference to the latest published version.

Three records connect that result to its production:

- **`report_refreshes`** records which output version the report read.
- **`outputs`** records that version's values and which run published it.
- **`runs`** records the run's status, code version and saved input identifier.

This query follows those connections:

```sql
SELECT r.run_id, r.code_version, r.input_snapshot_id
FROM report_refreshes AS f
JOIN outputs AS o ON o.output_version = f.output_version
JOIN runs AS r ON r.run_id = o.run_id
WHERE f.refresh_id = 'F1300';
```

| Run | Code version | Saved input |
|---|---|---|
| `R1205` | `completed-v1` | `S1205` |

The report therefore read the output of `R1205`. The code and input identifiers tell us what to inspect next. These table names are the simulation's own design; real tools may organise the same evidence differently.

In a live system, the job would record the input and code versions it actually used. The publisher would record the output version it made available, and the reporting tool would record the version it read. A database schema scan cannot supply those execution records.

## Reproduce the calculation from its evidence

`S1205` is a saved copy of the four input rows at 12:05. All four parcels were promised by noon. Compare their delivery times with the source at 13:00:

| Parcel | Saved input at 12:05 | Source at 13:00 |
|---|---|---|
| `D101` | 11:50 | 11:50 |
| `D102` | `NULL` | 12:20 |
| `D103` | 11:40 | 11:40 |
| `D104` | `NULL` | `NULL` |

At 12:05, only two parcels had arrived, both on time. By 13:00, a third had arrived late. In this example the records are complete at each observation; `NULL` means the parcel had not yet arrived.

The `code_versions` record for `completed-v1` retains the [SQL that was executed](../examples/lineage/completed-v1.sql). It excludes rows where `delivered_at` is `NULL`, counts the remaining rows, and counts how many arrived by their promised time.

Executing that saved code against `S1205` gives **2 on time out of 2 completed: 100%**. Executing it against the current source gives **2 out of 3: 66.7%**. The simulation checks both results with SQLite.

A version label alone is insufficient: we need the code it identifies. Reading today's query would not establish what an older run executed. Here the retained SQL, input rows and fixed UTC timestamp format are enough to repeat the calculation. Other jobs may also need their original parameters and software versions.

The earlier 100% was correct for its inputs. That does not make it current at 13:00. We have explained the disagreement, but still need to explain why the report kept the older result.

## Find the failure and recover

The run history supplies the next part of the story:

<figure class="worked-example incident-timeline" markdown="1">
<figcaption>Worked example · Why the old result remained available</figcaption>

| Time | Recorded event |
|---|---|
| 12:05 | `R1205` published `summary-R1205`: 2 completed, 2 on time, 100%. |
| 12:20 | The late delivery of `D102` was recorded in the source. |
| 12:30 | `R1230` failed before publication because the simulated destination did not permit writing. No new output replaced `summary-R1205`. |
| 13:00 | Refresh `F1300` read `summary-R1205`, displaying 100%. |

</figure>

The failed status alone would not identify the cause. This simulation also records the injected write-permission error. In a real investigation, the engineer would inspect the error and confirm the destination's permissions before making a change.

The failed run also would not prove that the report used an old result. The refresh record supplies that connection. Lineage shows the route from `deliveries` to the report; provenance connects its displayed 100% to a particular run, code version and set of inputs.

Suppose Service Analytics requires an output **published within the previous 30 minutes**. At 13:00, the report's output is 55 minutes old. Refreshing the page at 13:00 did not make the underlying result fresh. This publication-age check is useful, but a recent publication could still use stale source data; input freshness needs its own check.

The response has three parts: mark the report as outdated and notify its owner, correct the write problem, then verify a new publication and report refresh. The simulation demonstrates the last two steps:

| Time | Recovery record |
|---|---|
| 13:05 | Writing to the simulated destination is restored. |
| 13:10 | `R1310` uses `completed-v1` and a new saved input, `S1310`, to publish `summary-R1310`: 3 completed, 2 on time, 66.7%. |
| 13:12 | Refresh `F1312` reads `summary-R1310`. The report now displays 66.7%. |

No further deliveries arrive during this recovery. Reusing the earlier input `S1205` would simply reproduce 100%; the recovery run must read the updated source.

The publisher makes the saved output and the reference to the current output available in one database transaction. If publication fails, neither change remains. This avoids a report seeing a reference to a missing result. Different reporting systems need equivalent coordination; a successful calculation alone is not proof of publication.

Keep `F1300` and `summary-R1205` after recovery. They explain what readers saw earlier. Publishing a corrected current result should not silently rewrite that history. The local example does not send alerts or modify a real dashboard; those are responsibilities the operating team must implement.

<blockquote class="key-principle" markdown="1">

**Connect a reported number to the output, run, code and inputs that produced it. Then verify that recovery reaches the report.**

</blockquote>

## Decide how much history to keep

Saving four rows is cheap. Copying a large input for every run may be expensive. Where the storage system already retains immutable versions, a run can reference the version it read instead of creating another full copy. That only works while the referenced data remains available.

Suppose this team must investigate reports for 30 days. It could agree to keep input versions for 35 days, allowing five days for investigations opened near the deadline. Run records, code versions, outputs and report refreshes must remain available for at least the same investigations. These periods are a policy for this example, not a universal recommendation.

For example, retaining a separate 10 GB input copy every hour for 35 days requires **8.4 TB** before compression: 10 × 24 × 35 = 8,400 GB. Shared immutable versions may reduce that storage, but their expiry still limits replay. Metadata events also accumulate as runs and report refreshes increase.

Set an expiry policy and check that cleanup does not remove evidence still needed for an open investigation. Retained data needs appropriate access controls too.

After an input expires, the catalogue may still show which run and output a report used. It can no longer support replaying or independently checking that calculation from the original rows. Mark that limit explicitly: a saved identifier is not the same as saved evidence. The simulator refuses to replay a snapshot if its retained row count is incomplete; missing evidence is not an empty input.

## Check your understanding

**1. The code changed.** A later code version counts all four deliveries due, including unfinished parcels. You run it against `S1205` and get 50%. Does that show the recorded 100% was wrong? Which record should you check first?

<details class="further-detail" markdown="1">
<summary>Show answer · The code changed</summary>

No. The two versions answer different questions. `R1205` records `completed-v1`, which counts two completed deliveries, both on time: 2/2 = 100%. The later version counts all four deliveries due: 2/4 = 50%. Check the run's code-version reference and inspect that retained code. Replaying an old input with today's logic does not necessarily reproduce the original result.

</details>

**2. The input expired.** You still have `F1300`, `summary-R1205`, the run record and its SQL, but the rows in `S1205` have been deleted. What can you still establish, and what can you no longer verify?

<details class="further-detail" markdown="1">
<summary>Show answer · The input expired</summary>

You can trace the report to its stored 100%, identify the producing run and inspect its calculation rule. You cannot independently verify that the original input contained exactly two completed, on-time deliveries, or replay the original calculation from those rows. The current source is not a substitute: it includes a completion that was absent from the earlier input.

</details>

<details class="further-detail" markdown="1">
<summary>Further detail: records from dbt and OpenLineage</summary>

dbt runs SQL queries to build tables and views. Its [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json) describes these planned steps; `parent_map` and `child_map` record their immediate dependencies. Its [run results file](https://docs.getdbt.com/reference/artifacts/run-results-json) records statuses and timings. The [status schema](https://schemas.getdbt.com/dbt/run-results/v6.json) includes skipped steps, so appearing in this file does not prove a query ran. It does not supply a complete list of the inputs actually read by each query.

OpenLineage is an open standard for exchanging lineage records. A processing tool can send a `RunEvent` identifying a job, run, state and reported input and output datasets. Some tools report additional inputs in later events, so readers must combine events for the same run. Dataset names alone do not preserve the rows read. See the [object model](https://openlineage.io/docs/spec/object-model/) and [run cycle](https://openlineage.io/docs/spec/run-cycle/).

Useful retained fields include run identity, times, status, code version, input snapshot references, output version, publication outcome and report refresh reference. Their availability depends on the tools and retention arrangements; a lineage event alone does not guarantee them.

</details>
