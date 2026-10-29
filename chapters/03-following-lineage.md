# 3. Where did this number come from?

Service Analytics measures the percentage of **completed deliveries that arrived on time**. It excludes parcels still awaiting delivery. At 13:00, its Delivery performance report shows **100%**. What produced that number?

<figure class="chapter-video" aria-labelledby="chapter-video-title">
<figcaption id="chapter-video-title"><span>Watch the chapter</span><span class="chapter-video-duration">2 min 45 sec</span></figcaption>
<video controls playsinline preload="none" width="1280" height="720" poster="../assets/video/chapter-03/poster.jpg?v=be44a348a40d" aria-label="Where did this number come from?: narrated Chapter 3 explainer" aria-describedby="chapter-video-note">
<source src="../assets/video/chapter-03/chapter-03.mp4?v=0cd3b391d2d4" type="video/mp4">
<track kind="captions" src="../assets/video/chapter-03/captions.vtt?v=ce2ec34341d7" srclang="en" label="English">
Your browser cannot play this video. <a href="../assets/video/chapter-03/chapter-03.mp4?v=0cd3b391d2d4">Download the video</a> or <a href="../assets/video/chapter-03/transcript.txt?v=8fdf272bc046">read the transcript</a>.
</video>
<p class="chapter-video-note" id="chapter-video-note">The incident is invented and assumes complete records at the input capture time. Narration uses a synthetic voice.</p>
<p class="chapter-video-links"><a href="../assets/video/chapter-03/transcript.txt?v=8fdf272bc046">Read the transcript</a><a href="../assets/video/chapter-03/chapter-03.mp4?v=0cd3b391d2d4" download>Download video <span>(4.4 MB)</span></a></p>
</figure>

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

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=3&amp;record=report-refresh"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Find refresh <code>F1300</code>’s <code>output_version</code>, then follow that value to <strong>Published output</strong>. Compare refresh and publication times.</li>
<li>Follow the output’s <code>run_id</code> to <strong>Run</strong>. Note the input snapshot and code version it used.</li>
</ol>
<p><strong>Think about it:</strong> Which execution explains the displayed 100%, and would the current deliveries table be enough to reproduce it?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p><code>F1300</code> read <code>summary-R1205</code>, published at 12:05 and refreshed at 13:00. Its producing execution was <code>R1205</code>, using <code>S1205</code> and <code>completed-v1</code>. Reproduction needs the retained input rows and executed code, not just today’s table or the version labels. The matching identifiers establish the chain behind this particular result.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
