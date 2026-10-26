# 7. Using metadata to make decisions

Metadata helps someone choose a dataset, judge a result or prepare a change. Each decision needs different evidence: a definition explains what a measure counts; a quality check describes particular records; a dependency points to a possible consumer.

## Find the measure that answers the question

Delivery Operations asks: “Of all parcels due by noon, how many arrived on time?” Searching for “on-time delivery” finds the `on_time_completed` view and Service Analytics' Delivery performance report. Their definitions determine whether either fits.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Choosing a measure for the operations meeting</figcaption>

Use the same four complete parcel records at 13:00: two arrived on time, one arrived late and one remains unfinished.

| Candidate | What it tells us |
|---|---|
| Completed-delivery view | Excludes the unfinished parcel: 2 out of 3 gives 66.7%. It answers a different question. |
| Delivery performance report | Uses the completed-delivery rule; at 13:00 it still displays the older 100%. Refreshing cannot change its definition. |
| Agreed all-due definition | Includes all four parcels due: 2 out of 4 gives 50.0%. This is the required rule; a working calculation still needs verification. |

</figure>

Delivery Operations confirms which parcels the measure must include. The reporting engineer must check that a proposed calculation includes unfinished parcels and reproduces 50.0%, then verify which published output reaches the meeting.

## Separate quality checks from meaning

The following review and decision are illustrative records for this teaching example, not additional results from the incident simulation.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative quality review</span><span class="record-source">Four-parcel input at 13:00 UTC, 19 October 2026</span></figcaption>
<dl>
<div><dt>Source</dt><dd><code>deliveries</code>; teaching input <code>decision-input-1300</code></dd></div>
<div><dt>Scope</dt><dd>All four parcels due by noon</dd></div>
<div><dt>Checked at</dt><dd>13:05 UTC, 19 October 2026</dd></div>
<div class="record-focus"><dt>Identifier check</dt><dd><strong>Four rows, four distinct delivery identifiers</strong></dd></div>
<div class="record-focus"><dt>Time checks</dt><dd><strong>Four promised times present; one delivery time empty, allowed for an unfinished parcel</strong></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this supports</strong> The checked input has no duplicate delivery identifiers or missing promised times. Its version and cutoff identify the records covered.</p>
<p class="evidence-limit"><strong>What it does not establish</strong> These checks do not prove the times are accurate, the measure answers the meeting's question or the report read this input. A correctly calculated 66.7% still uses the wrong denominator for that question.</p>

Currency requires separate evidence. The incident's 13:00 refresh read `summary-R1205`, containing 100%, after the 12:30 run failed. A successful quality check cannot establish that a later publication reached the report.

## Scope a proposed change

Suppose `promised_at` changes from the original customer promise to the latest revised promise. A parcel arriving at 12:20 is late against its original noon promise but on time against a revised 12:30 promise. The change can also alter which parcels are due by noon. The column's name and type would reveal neither effect.

The dependency path identifies `build_delivery_summary`, `delivery_summary` and Delivery performance for review. Both Delivery Operations and Service Analytics must compare their measures under the two promise rules before the engineer changes the source.

Recorded dependencies may omit a monthly report or downloaded spreadsheet. Record which systems and dates were checked, ask the source owner about gaps, and assign someone to investigate unresolved uses.

## Leave a decision someone can act on

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative meeting decision</span><span class="record-source">Delivery Operations review</span></figcaption>
<dl>
<div class="record-focus"><dt>Decision</dt><dd><strong>Use the all-due rule; expected four-parcel result: 50.0%</strong></dd></div>
<div><dt>Current gap</dt><dd>No verified all-due publication is attached</dd></div>
<div><dt>Next action and owner</dt><dd>Reporting engineer verifies the calculation and attaches the published output identifier and report refresh evidence before the next meeting</dd></div>
<div><dt>Definition owner</dt><dd>Delivery Operations confirms the denominator and original-promise rule</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What someone can do next</strong> The decision names the required rule, missing evidence and responsible people. It remains pending until the calculation and publication are verified.</p>

## Core points

- **Choose data by the question it answers.** Names alone do not establish the required definition.
- **Quality checks support specific claims.** Record their scope; meaning and currency need separate evidence.
- **Dependencies identify places to investigate.** Collection may miss consumers.
- **Leave an actionable decision.** Name the evidence gap, next action and owner.
