# 4. Why is this report out of date?

The report refreshed at 13:00 but read a result saved at 12:05: **two completed deliveries, both on time, giving 100%**. At 12:20, a third parcel had arrived late. The current delivery records therefore gave **2 out of 3: 66.7%**.

The calculation rule had not changed. The report was displaying an older result. Why had the next calculation not replaced it?

This continues the invented incident on 19 October 2026. All times are UTC.

## Why was the report still using the old result?

The next run, at 12:30, failed before publishing a new result. Its recorded error supplies a cause to investigate.

<figure class="metadata-record" data-table="runs">
<figcaption><span class="record-kind">Later run</span><span class="record-source">Recorded in <code>runs</code></span></figcaption>
<dl>
<div><dt><code>run_id</code></dt><dd><code>R1230</code></dd></div>
<div><dt><code>finished_at</code></dt><dd><code>2026-10-19 12:30</code></dd></div>
<div class="record-focus"><dt><code>status</code></dt><dd><strong><code>failed</code></strong></dd></div>
<div class="record-focus"><dt><code>error</code></dt><dd><strong><code>injected fault: destination write permission denied</code></strong></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The 12:30 run encountered a write-permission error. In this simulation the fault is deliberate; it prevents publication, leaving no output for <code>R1230</code>.</p>
<p class="evidence-limit"><strong>What it does not tell us</strong> A failed status alone would not show what the report displayed. The report’s refresh record <code>F1300</code> supplies that evidence: it read <code>summary-R1205</code>, the output saved at 12:05.</p>

In a live system, an engineer would check the error and destination permissions before changing them. The record identifies a problem to investigate; it does not repair it.

## What confirms the report recovered?

After the simulated permission problem is removed, a new run uses the same calculation with updated inputs and publishes 66.7%. No further deliveries arrive during recovery. The output and refresh records show whether that result reached the report:

| Record | Before recovery | After recovery |
|---|---|---|
| Published output: `output_version` | `summary-R1205` | `summary-R1310` |
| Published output: `published_at` | 12:05 | 13:10 |
| Published output: `percentage` | 100.0 | **66.7** |
| Report refresh: `refresh_id` | `F1300` | `F1312` |
| Report refresh: `refreshed_at` | 13:00 | 13:12 |
| Report refresh: `output_version` | `summary-R1205` | **`summary-R1310`** |

<p class="evidence-reading"><strong>What confirms recovery</strong> The 13:12 refresh read the newly published output containing 66.7%. A successful run alone would not establish this.</p>

## What if the run succeeds but the number is wrong?

A successful run means the process completed according to its own success criteria. It does not establish that its calculation follows the agreed definition. Consider a separate, hypothetical fault: a developer removes the filter that excludes unfinished deliveries from the completed-delivery measure.

At 13:00, the four delivery records contain two on-time arrivals, one late arrival and one unfinished parcel. The changed calculation divides by all four rows and produces **50.0%**, although Service Analytics expects **66.7%**. Here 50.0% happens to answer Delivery Operations' question; it is wrong for this report.

<figure class="worked-example" markdown="1">
<figcaption>Illustrative debugging evidence · A successful run with the wrong denominator</figcaption>

| Evidence to follow | What the engineer inspects |
|---|---|
| Report refresh → output → run | Identify the execution behind the displayed number before opening its logs. |
| Run → retained code | Compare the SQL version with the previous version: `WHERE delivered_at IS NOT NULL` has disappeared. |
| Output column `percentage` → input columns | The numerator compares `delivered_at` with `promised_at`; the denominator now counts every row. |
| Run identifier in execution logs | Inspect messages from this execution and its individual attempts, rather than a different retry or today's run. |

</figure>

This is **column-level lineage**: it connects an output field to the input fields and transformations that contribute to it. Row filters and joins matter too, because they change which records contribute. A list of table dependencies alone cannot reveal the missing filter. A parser may miss dynamic SQL or external code, so retain the executed logic and state what the lineage covers.

The engineer checks the suspected cause against the saved input: restoring the filter gives 2 out of 3. A corrected publication and report refresh still need verification. Logs help diagnose the execution; retained inputs and code establish why its calculation produced that result.

## Keep the earlier evidence

Publishing the new result should not erase the old output or its report refresh record. They explain what readers saw at 13:00. The later 66.7% does not make the earlier calculation incorrect for its inputs.

Agree how far back the team needs to investigate reports, then retain the necessary input data, code, run records, outputs and refresh records for that period. Existing stored versions may avoid making extra copies, provided they remain available.

If the original inputs are deleted, a run record may still identify their source, but it cannot supply the missing rows. We can trace the result's recorded history without being able to reproduce its calculation.

In a working system, the reporting tool records which output it read, the publisher identifies the output it made available, and the processing job records its inputs and code version. A database schema scan cannot supply those execution records. [Chapter 5](05-collecting-metadata.md) explains how to bring records from different systems together.

*Supporting material: the [simulation reference and source code](../examples/lineage/README.md) show how the records in Chapters 3 and 4 were produced. No code execution is required to read either chapter.*

## Core points

- **Refreshing a report does not guarantee fresh data.** It may still read an older saved result after a processing failure.
- **Verify that recovery reaches the report.** A successful run is not enough: the report must read the newly published output.
- **A successful run can use the wrong logic.** Trace the affected field, inspect filters and joins, and correlate logs with the producing execution.
- **Keep the evidence needed to explain earlier reports.** Reproducing an old calculation requires its inputs and code, not just references to them.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=4&amp;record=report-refresh"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Compare <code>F1300</code>’s refresh time with its linked <strong>Published output</strong>’s publication time and percentage.</li>
<li>Follow that output to <strong>Run</strong>. Note which execution succeeded; compare these map examples with the recovery table in this chapter.</li>
</ol>
<p><strong>Think about it:</strong> Do the map’s records establish recovery? Which publication and refresh references would you need?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>The map shows the earlier evidence: <code>F1300</code> at 13:00 read <code>summary-R1205</code>, published at 12:05 with 100.0%. Its successful run <code>R1205</code> does not establish recovery. The chapter’s later evidence connects <code>F1312</code> to <code>summary-R1310</code>, containing 66.7%. That new publication and the refresh that read it are both needed; they are not additional examples in this map.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
