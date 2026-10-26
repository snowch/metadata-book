# 3. Where did this number come from?

Service Analytics measures the percentage of **completed deliveries that arrived on time**. It excludes parcels still awaiting delivery. At 13:00, its Delivery performance report shows **100%**. What produced that number?

## Lineage and provenance

<div class="definition-box" markdown="1">

**Lineage**

Records where data comes from, how it is transformed, and which datasets or reports depend on it.

</div>

<div class="definition-box" id="provenance" markdown="1">

**Provenance**

Records the history of a particular dataset or result: who or what created or changed it, when, and using which sources and methods.

</div>

Lineage emphasises **data flow**; provenance emphasises **creation and change history**. Both can describe transformations and the people or systems involved, so the distinction is not simply “how” versus “who.” The terms overlap in practice; lineage tools can also capture provenance.

## Follow the route

A scheduled job calculates the percentage from the delivery records and saves the result. The report reads that saved result whenever someone refreshes it. Refreshing the report does not rerun the calculation.

<figure class="lineage-diagram" aria-labelledby="lineage-caption">
<figcaption id="lineage-caption">How the number reaches the report</figcaption>
<ol>
<li><span class="flow-role">Source</span>Delivery records<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Calculation</span>Scheduled job<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Stored output</span>Saved percentage<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Report</span>Delivery performance</li>
</ol>
</figure>

This lineage shows the route to the report. To explain its particular 100%, we need the run, inputs and processing code that produced it. Looking only at the latest successful run could lead us to a result the report never read.

The following cards show selected records from an invented incident, checked with SQLite. Field names belong to this example; real tools may use different names. All times are UTC on 19 October 2026.

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

The retained [calculation for `completed-v1`](../examples/lineage/completed-v1.sql) excludes unfinished deliveries, then divides the number delivered on time by the number completed. All four parcels were promised by noon. These are the delivery rows it read, with timestamps shortened to show the time:

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

The records now connect the report to a specific calculation and its inputs. That is provenance for the displayed number. We have established why the saved result was 100%; [Chapter 4](04-outdated-reports.md) examines whether it was still current when readers saw it.

## Core points

- **Lineage shows the route; provenance explains a result's history.** The terms overlap, but a dependency path alone does not identify the run behind a displayed number.
- **Follow the report to its saved output, then to the producing run.** The matching identifiers connect the records.
- **Check the run's inputs and code.** Today's data and calculation may differ from those that produced the result.
