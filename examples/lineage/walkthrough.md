# Worked example: the metadata behind an outdated report

The Delivery performance report shows **100%** at 13:00. The current delivery records give **66.7%**. Both measure the percentage of completed deliveries that arrived on time. Which records explain the difference?

These are selected fields from the book's local simulation, presented as readable cards. The incident is invented; the values are computed and checked with SQLite. They are not exports from a production tool. All times are UTC on 19 October 2026.

## Which result did the report read?

Start with the refresh record. `output_version` identifies the saved result read by this refresh.

<figure class="metadata-record" data-table="report_refreshes">
<figcaption><span class="record-kind">Report refresh</span><span class="record-source">Recorded in <code>report_refreshes</code></span></figcaption>
<dl>
<div><dt><code>refresh_id</code></dt><dd><code>F1300</code></dd></div>
<div><dt><code>report_name</code></dt><dd><code>Delivery performance</code></dd></div>
<div><dt><code>refreshed_at</code></dt><dd><code>2026-10-19 13:00</code></dd></div>
<div class="record-focus"><dt><code>output_version</code></dt><dd><strong><code>summary-R1205</code></strong></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The report refreshed at 13:00, but it read <code>summary-R1205</code>. The refresh time alone does not tell us when that result was produced.</p>

Follow that output identifier to the published result. `run_id` identifies the execution that produced it.

<figure class="metadata-record" data-table="outputs">
<figcaption><span class="record-kind">Published output</span><span class="record-source">Recorded in <code>outputs</code></span></figcaption>
<dl>
<div><dt><code>output_version</code></dt><dd><code>summary-R1205</code></dd></div>
<div class="record-focus"><dt><code>run_id</code></dt><dd><strong><code>R1205</code></strong></dd></div>
<div class="record-focus"><dt><code>published_at</code></dt><dd><strong><code>2026-10-19 12:05</code></strong></dd></div>
<div><dt><code>percentage</code></dt><dd><code>100.0</code></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The displayed 100% came from run <code>R1205</code>, published 55 minutes before the refresh. Matching <code>output_version</code> connects these two records.</p>
<p class="evidence-limit"><strong>What it does not tell us</strong> A stored percentage does not establish whether its calculation was correct. For that, we need the inputs and code.</p>

## Which inputs and calculation produced 100%?

The run record identifies both. A **snapshot** is a retained copy of the input data at a particular time; `input_snapshot_id` tells us which copy this run read.

<figure class="metadata-record" data-table="runs">
<figcaption><span class="record-kind">Producing run</span><span class="record-source">Recorded in <code>runs</code></span></figcaption>
<dl>
<div><dt><code>run_id</code></dt><dd><code>R1205</code></dd></div>
<div><dt><code>job_name</code></dt><dd><code>build_delivery_summary</code></dd></div>
<div><dt><code>status</code></dt><dd><code>success</code></dd></div>
<div class="record-focus"><dt><code>input_snapshot_id</code></dt><dd><strong><code>S1205</code></strong></dd></div>
<div class="record-focus"><dt><code>code_version</code></dt><dd><strong><code>completed-v1</code></strong></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> Inspect saved input <code>S1205</code> and retained code <code>completed-v1</code>. The current table and today’s code may differ from what this run used.</p>

The retained [calculation for `completed-v1`](completed-v1.sql) excludes unfinished deliveries, then divides the number delivered on time by the number completed. Here are the actual delivery rows it read, with timestamps shortened to show the time:

<figure class="worked-example" markdown="1">
<figcaption>Saved input · S1205, captured at 12:05</figcaption>

| Delivery | Promised by | Delivered at |
|---|---|---|
| `D101` | 12:00 | 11:50 |
| `D102` | 12:00 | `NULL` |
| `D103` | 12:00 | 11:40 |
| `D104` | 12:00 | `NULL` |

</figure>

These rows are the input data; the run's reference to them is metadata. In this complete example, `NULL` means the parcel had not yet arrived. The calculation includes D101 and D103: **2 on time out of 2 completed = 100%**.

D102 arrived late at 12:20. The current data therefore includes three completed deliveries, two on time: **66.7%**. The earlier 100% was correct for the earlier inputs.

<p class="evidence-limit"><strong>What the references cannot do</strong> If the original rows or code have been deleted, their identifiers cannot reproduce the calculation. The references can still help trace the recorded history, but reproducing the calculation requires the original evidence too.</p>

## Why was the report still using the old result?

The next run failed. Its recorded error supplies a cause to investigate.

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
<p class="evidence-limit"><strong>What it does not tell us</strong> A failed status alone would not show what the report displayed. The 13:00 refresh record supplies that evidence: it still points to the 12:05 output.</p>

In a live system, an engineer would check the error and destination permissions before changing them. The record identifies a problem to investigate; it does not repair it.

## What confirms the report recovered?

After the simulated permission problem is removed, a new run reads the updated inputs and publishes 66.7%. No further deliveries arrive during recovery. The output and refresh records show whether that result reached the report:

| Record | Before recovery | After recovery |
|---|---|---|
| Published output: `output_version` | `summary-R1205` | `summary-R1310` |
| Published output: `published_at` | 12:05 | 13:10 |
| Published output: `percentage` | 100.0 | **66.7** |
| Report refresh: `refresh_id` | `F1300` | `F1312` |
| Report refresh: `refreshed_at` | 13:00 | 13:12 |
| Report refresh: `output_version` | `summary-R1205` | **`summary-R1310`** |

<p class="evidence-reading"><strong>What confirms recovery</strong> The 13:12 refresh read the newly published output containing 66.7%. A successful run alone would not establish this. Keep the earlier records too: they explain what readers saw at 13:00.</p>

## Where these records come from

In a working system, the reporting tool must record which output it read, the publisher must identify the output it made available, and the processing job must record its inputs and code version. A database schema scan cannot supply those execution records. Tools may use different field names; the essential connections remain the same.

[Chapter 3](../../chapters/03-following-lineage.md) explains lineage and provenance. Continue to [Chapter 4](../../chapters/04-collecting-metadata.md) for collecting records from several systems.

*Supporting material: the [simulation reference and source code](README.md) show how these records were produced. Nothing needs to be run to follow this example.*
