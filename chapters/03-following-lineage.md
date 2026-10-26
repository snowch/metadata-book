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

A diagram can show that a report depends on a table and a processing job. To explain the number displayed in that report, we also need to know which run produced it and which data that run used.

## Follow the route

Suppose another team, Service Analytics, uses the completed-delivery measure: the first question in Chapter 1's table, also calculated by the view in Chapter 2. The SQLite view `on_time_completed` evaluates its query whenever it is read. Now suppose a scheduled job, `build_delivery_summary`, uses that same calculation to write a stored table called `delivery_summary`. Publishing a new result makes it available to reports. If a run fails before publishing, reports can still read the previous result.

<figure class="lineage-diagram" aria-labelledby="lineage-caption">
<figcaption id="lineage-caption">Declared dependency path</figcaption>
<ol>
<li><span class="flow-role">Source table</span><code>deliveries</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Scheduled job</span><code>build_<wbr>delivery_<wbr>summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Stored result</span><code>delivery_summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Report</span>Delivery performance</li>
</ol>
</figure>

The route identifies the job to investigate. To explain a displayed value, we also need records connecting a particular execution, its published output and the report that read it.

## Reconstruct the report's evidence

In this invented incident, the report shows 100% at 13:00 on 19 October 2026. The current source gives 66.7%. Both calculations use the same rule: count on-time deliveries among completed deliveries. We need to check whether they used the same records. All times below are UTC on that date.

<figure class="worked-example incident-timeline" markdown="1">
<figcaption>Worked example · The records behind a stale result</figcaption>

| Time | Evidence |
|---|---|
| 12:05 | Successful run `R1205` captured all four delivery rows. Two were completed on time; the other two delivery times were NULL. It published `summary-R1205`: 2 completed, 2 on time, 100%. |
| 12:20 | A third parcel's late completion was recorded. The current source now has 3 completed deliveries, 2 on time: 66.7%. |
| 12:30 | Run `R1230` failed before publishing. The previous output version remained available. |
| 13:00 | The report refresh explicitly read `summary-R1205`, displaying 100%. |

</figure>

The saved input rows show what the successful run read: all four deliveries, but only two with a delivery time. Both were on time, giving 100%. Reading the source after 12:20 gives a different result because a third completion has been recorded. The current table alone cannot reproduce what the earlier run saw.

The publication record identifies the stored output, and the refresh record connects that version to the report. Together they show that the report displayed the result from an earlier successful run. The failed run alone would not prove that connection, and these records do not establish why the job failed.

Lineage shows the route from `deliveries` to the report. Provenance identifies the run and input records behind the displayed 100%.

<blockquote class="key-principle" markdown="1">

**To explain a reported number, connect it to a particular run and its inputs.**

</blockquote>

## Keep the evidence connected

Keep a copy of the input rows, or a link to a saved version, along with the run and publication records and the report's refresh record. Check that they connect the inputs, run, output and report before using them to explain the number. Lineage does not decide whether the metric's definition answers the right business question.

<details class="further-detail" markdown="1">
<summary>Further detail: records from dbt and OpenLineage</summary>

dbt runs SQL queries to build tables and views. Its [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json) describes these planned steps; `parent_map` and `child_map` record their immediate dependencies. Its [run results file](https://docs.getdbt.com/reference/artifacts/run-results-json) records statuses and timings. The [status schema](https://schemas.getdbt.com/dbt/run-results/v6.json) includes skipped steps, so appearing in this file does not prove a query ran. It does not supply a complete list of the inputs actually read by each query.

OpenLineage is an open standard for exchanging lineage records. A processing tool can send a `RunEvent` identifying a job, run, state and reported input and output datasets. Some tools report additional inputs in later events, so readers must combine events for the same run. Dataset names alone do not preserve the rows read. See the [object model](https://openlineage.io/docs/spec/object-model/) and [run cycle](https://openlineage.io/docs/spec/run-cycle/).

Useful retained fields include run identity, times, status, code version, input snapshot references, output version, publication outcome and report refresh reference. Their availability depends on the tools and retention arrangements; a lineage event alone does not guarantee them.

</details>
