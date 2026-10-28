# 8. Choosing and operating a metadata platform

A metadata platform should help a team complete a task it currently struggles with. Start with a small collection whose answers are known, then judge what a reader can establish.

## Define a bounded pilot

Consider a one-week pilot for the reporting engineer and a Delivery Operations reviewer. Its two questions are concrete: which measure belongs in the operations meeting, and why did Delivery performance show 100% at 13:00 on 19 October?

Include both definitions, the `deliveries` and `on_time_completed` structure, the `build_delivery_summary` dependency path, and the incident's run, publication and refresh records. Preserve references to retained inputs and code. The expected answers are the all-due rule, giving 50.0% for the four parcels, and a refresh that read `summary-R1205` after a later run failed.

The assessment below is **an invented teaching outcome**, showing how a completed pilot could inform a decision. It does not report a real pilot or tests of DataHub or OpenMetadata.

## Read the assessment

In this scenario, reviewed documents and SQLite records sit behind the team's existing access controls. A reviewer who did not assemble them follows the evidence.

Metadata can reveal protected information even when a reader cannot open the underlying table: a column name may reveal what is collected, SQL may contain a customer identifier, and sample values may expose personal details. Decide who may see those descriptions, queries and samples, including through search, exports and APIs. Permission to discover a dataset does not automatically grant permission to read its rows.

<figure class="worked-example" markdown="1">
<figcaption>Illustrative pilot assessment · Observations and gaps</figcaption>

| Check | Recorded outcome |
|---|---|
| Choose the measure | **Pass.** Reviewer selects all-due and explains 2 out of 4 = 50.0%; recognises that completed deliveries give 66.7%. |
| Explain the incident | **Pass.** Reviewer traces the refresh to the output, run, retained input and code, then finds the later failed run. Export preserves source identifiers, observation times and version references. |
| Recognise outdated collection | **Pass.** A simulated collection failure leaves the last successful observation time visible beside a failure notice. Reviewer recognises the records may be outdated. Job and report updates still require manual work. |
| Respect access | **Pass for tested accounts and paths.** Permitted reviewer opens the retained evidence. Restricted account cannot retrieve protected descriptions through search, direct links or the API. Repeat checks when permissions or interfaces change. |

</figure>
<p class="evidence-reading"><strong>What this supports</strong> In the scenario, the small arrangement answers both questions and exposes collection failure. The reviewer can open the evidence, not merely see links to it.</p>
<p class="evidence-limit"><strong>What remains unknown</strong> These observations do not establish coverage of another database, report tool or permission model. No catalogue product has been assessed.</p>

Coverage explains the remaining work. Here, a database collector supplies table and view structure; the engineer enters job dependencies, publications and report refreshes by hand. A collector reads metadata from a source, but its presence does not establish which records it supplies. Exported identifiers, times and versions must remain connected to their sources so a move preserves the evidence chain.

## Budget for continuing work

The illustrative team sets a budget of two engineer-hours per week for collection and link maintenance. It agrees that metadata changes must appear within one working day. The reporting engineer owns collection failures and checks the age of the last successful observation; Delivery Operations owns the all-due definition, and Service Analytics owns the completed-delivery definition.

The team must also maintain access credentials and retain the history needed to explain past reports. Collector upgrades trigger another check of identifiers, fields, permissions and evidence links. The pilot's acceptable effort does not establish the cost of wider coverage.

## Record the choice

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative platform decision</span><span class="record-source">End-of-week pilot review</span></figcaption>
<dl>
<div class="record-focus"><dt>Decision</dt><dd><strong>Keep reviewed documents and SQLite for the two pilot questions</strong></dd></div>
<div><dt>Observed effort</dt><dd>90 minutes of weekly maintenance; within the two-hour budget</dd></div>
<div><dt>Observed freshness</dt><dd>Changes recorded the same working day; within the one-day limit</dd></div>
<div><dt>Remaining gap</dt><dd>Job and report records depend on manual updates; additional sources are untested</dd></div>
<div><dt>Next review</dt><dd>Reporting engineer reviews weekly; trial a catalogue if updates take longer than one working day or maintenance exceeds two hours per week</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>Why this choice follows</strong> The smallest arrangement passes the scoped checks within budget. Wider adoption needs evidence that it remains useful and maintainable.</p>

If a catalogue trial becomes worthwhile, verify exact source and version support in the [DataHub documentation](https://docs.datahub.com/docs/) or [OpenMetadata documentation](https://docs.open-metadata.org/). Expand to one additional report only after the trial passes the same checks and measurably reduces work. Fix missing evidence or access gaps before expanding.

## Core points

- **Start with a small task and known answers.** Assess what an independent reader can establish.
- **Check coverage, export and access.** Record manual work and untested sources.
- **Budget for ongoing ownership and freshness.** Maintenance continues after setup.
- **Choose the smallest arrangement that passes.** Expand only with evidence that it works and reduces effort.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=8&amp;record=collection-run"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Read the collector’s scope and claim. Name one supported fact and one missing kind of evidence.</li>
<li>Select <strong>Responsible team</strong>. Compare its definition responsibility with the chapter’s assignment of collection maintenance to the reporting engineer.</li>
</ol>
<p><strong>Think about it:</strong> Would installing this collector establish complete incident coverage or transfer definition ownership to its operator?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>No. This scan supports a structural observation about <code>prod/parcels/delivery_summary</code>: <code>percentage</code> exists. It does not supply the run-to-output-to-refresh chain or establish a complete scan. Delivery Operations confirms the all-due denominator and original-promise rule; collection maintenance is separate work. A pilot should test evidence access and maintenance against its budget. The map records do not measure that effort or assess a catalogue product.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
