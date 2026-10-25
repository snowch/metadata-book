# 3. Following a number to its source

Lineage connects data's inputs, processing steps and outputs. It gives us a route from a number in a report back through the work that produced it. Following that route requires two kinds of evidence: declared dependencies describe how data is intended to flow; execution records describe what happened in a particular run.

## Follow the route

Continue with the parcel company's completed-delivery measure from Chapter 1. The SQLite view `on_time_completed` evaluates its query whenever it is read. Now suppose a scheduled job, `build_delivery_summary`, writes a stored table called `delivery_summary`. That result changes when a new version is published, so it can lag behind its source.

<figure class="lineage-diagram" aria-labelledby="lineage-caption">
<figcaption id="lineage-caption">Declared dependency path</figcaption>
<ol>
<li><span class="flow-role">Source table</span><code>deliveries</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Scheduled job</span><code>build_<wbr>delivery_<wbr>summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Stored result</span><code>delivery_summary</code><span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Report</span>Delivery performance</li>
</ol>
</figure>

The route identifies the transformation to investigate. To explain a displayed value, we also need records connecting a particular execution, its published output and the report that read it.

## Reconstruct the report's evidence

In this invented incident, the report shows 100% at 13:00 on 19 October 2026. The current source gives 66.7%. Both calculations count on-time deliveries among completed deliveries, so a different denominator does not explain the disagreement. All times below are UTC on that date.

<figure class="worked-example incident-timeline" markdown="1">
<figcaption>Worked example · The records behind a stale result</figcaption>

| Time | Evidence |
|---|---|
| 12:05 | Successful run `R1205` captured all four delivery rows. Two were completed on time; the other two delivery times were NULL. It published `summary-R1205`: 2 completed, 2 on time, 100%. |
| 12:20 | A third parcel's late completion was recorded. The current source now has 3 completed deliveries, 2 on time: 66.7%. |
| 12:30 | Run `R1230` failed before publishing. The previous output version remained available. |
| 13:00 | The report refresh explicitly read `summary-R1205`, displaying 100%. |

</figure>

The captured input establishes what the successful run knew: all four parcels were present, but only two had recorded completions. Its 100% follows from those records. Reading the source after 12:20 gives a different result because a third completion has been recorded. The current table alone cannot reproduce what the earlier run saw.

The publication record identifies the stored output, and the refresh record connects that version to the report. Together they support the diagnosis: the report displayed a stale successful output. The failed run alone would not prove that connection, and these records do not establish why the job failed.

<blockquote class="key-principle" markdown="1">

**To explain a reported number, connect it to a particular run and its inputs.**

</blockquote>

## Read tool records with the same distinction

Real tools provide parts of this evidence. dbt is a transformation tool whose manifest describes project resources and their dependencies. Its run results record execution statuses and timings. A resource can appear as skipped, so its presence in the results does not by itself mean its transformation ran.

OpenLineage is an open standard for exchanging lineage records. Processing tools can report a job's run and its input and output datasets through integrations. These records help connect executions across systems, but reported dataset names do not guarantee complete snapshots of the rows read.

For an investigation like this one, preserve captured inputs or references to retained snapshots, run and publication records, and the report's version reference. Check that those references join the same chain before explaining the number. Lineage does not decide whether the metric's definition answers the right business question.

<details class="further-detail" markdown="1">
<summary>Further detail: artifact fields and accumulating events</summary>

In dbt's [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json), `parent_map` and `child_map` record immediate dependencies. The [run results artifact](https://docs.getdbt.com/reference/artifacts/run-results-json) records resource statuses and timings; its [status schema](https://schemas.getdbt.com/dbt/run-results/v6.json) includes skipped resources. It does not supply a complete observed input-dataset list for each model.

An OpenLineage `RunEvent` identifies a job, run, state and reported inputs and outputs. Some integrations report additional inputs in later events, so consumers must combine events for the same run. See the [object model](https://openlineage.io/docs/spec/object-model/) and [run cycle](https://openlineage.io/docs/spec/run-cycle/).

Useful retained fields include run identity, times, status, code version, input snapshot references, output version, publication outcome and report refresh reference. Their availability depends on the tools and retention arrangements; a lineage event alone does not guarantee them.

</details>
