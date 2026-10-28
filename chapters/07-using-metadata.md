# 7. Using metadata to make decisions

Metadata helps someone choose a dataset, judge a result or prepare a change. Each decision needs different evidence: a definition explains what a measure counts; a quality check result describes particular records; a dependency points to a possible consumer.

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

## Make the right candidate discoverable

A new analyst might search for “late parcels” instead of “on-time delivery.” A catalogue can connect those terms through a maintained business glossary, but it must still distinguish completed deliveries from all deliveries due. Synonyms help discovery; they do not make different definitions equivalent.

An illustrative search result should expose enough information to reject an unsuitable candidate before opening its data:

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative search result</span><span class="record-source">Completed-delivery measure</span></figcaption>
<dl>
<div><dt>Title and search terms</dt><dd>On-time completed deliveries; delivery performance; late parcels</dd></div>
<div class="record-focus"><dt>Scope</dt><dd><strong>Completed deliveries only. Excludes unfinished parcels.</strong></dd></div>
<div><dt>Responsible team</dt><dd>Service Analytics; contact for the definition</dd></div>
<div><dt>Status and currency</dt><dd>Active definition; report publication must be checked separately</dd></div>
<div><dt>Access</dt><dd>Request access to the report through the reporting team; search visibility does not grant data access</dd></div>
</dl>
</figure>

Clear titles, descriptions, glossary terms and active or retired status make discovery useful. Search ranking and popularity can help order results, but neither establishes suitability.

## Judge suitability for this use

“Trusted” needs a purpose and supporting evidence. For the operations meeting, ask whether the definition includes every parcel due, whether the input covers the required cutoff, which quality checks ran, and which output reached the report. Also check that the intended use is permitted. A dataset can be suitable for one task and unsuitable for another.

## Record what producers and consumers agree

A **data contract** records what a producer agrees to provide and what consumers can depend on: structure, meaning, quality rules, delivery timing and how changes are handled. A schema alone does not capture that agreement.

The contract, quality review and meeting decision below are illustrative teaching records, not additional results from the incident simulation.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative data contract</span><span class="record-source">deliveries-v1</span></figcaption>
<dl>
<div><dt>Dataset and parties</dt><dd><code>deliveries</code>; the reporting engineer supplies snapshots to Delivery Operations and Service Analytics</dd></div>
<div><dt>Structure</dt><dd><code>delivery_id TEXT</code>, <code>promised_at TEXT</code>, <code>delivered_at TEXT</code>; timestamps use <code>YYYY-MM-DD HH:MM</code> in UTC</dd></div>
<div class="record-focus"><dt>Meaning</dt><dd><strong>One row per delivery. <code>promised_at</code> is the original customer promise; an unfinished delivery has no completion time.</strong></dd></div>
<div><dt>Quality rules</dt><dd><code>delivery-ids-unique-v1</code>: no duplicate delivery identifiers. Identifiers and promised times must be present.</dd></div>
<div><dt>Delivery commitment</dt><dd>A daily snapshot of records known at 13:00 UTC, available by 13:05 UTC</dd></div>
<div><dt>Changes</dt><dd>Agree changes to structure or meaning with both consuming teams before publishing a new contract version</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this settles</strong> Both teams can rely on the same original-promise field while choosing different denominators for their measures.</p>
<p class="evidence-limit"><strong>What still needs evidence</strong> Writing a commitment does not enforce it. Checks, delivery records and consumer review establish whether it was met.</p>

## Separate quality checks from meaning

A **quality rule** states what should hold. A **quality check result** records what was observed, on which input, when, and against which rule version. For example, `delivery-ids-unique-v1` requires zero duplicate delivery identifiers; the review below records the count actually found.

Uniqueness checks look for duplicates; completeness checks look for missing required values. Freshness checks compare an update or delivery time with an agreed deadline. Passing one kind of check says nothing about the others.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative quality review</span><span class="record-source">Four-parcel input at 13:00 UTC, 19 October 2026</span></figcaption>
<dl>
<div><dt>Source</dt><dd><code>deliveries</code>; teaching input <code>decision-input-1300</code></dd></div>
<div><dt>Scope</dt><dd>All four parcels due by noon</dd></div>
<div><dt>Checked at</dt><dd>13:05 UTC, 19 October 2026</dd></div>
<div><dt>Identifier rule</dt><dd><code>delivery-ids-unique-v1</code>; expected duplicate count: zero</dd></div>
<div class="record-focus"><dt>Identifier check</dt><dd><strong>Four rows, four distinct delivery identifiers</strong></dd></div>
<div class="record-focus"><dt>Time checks</dt><dd><strong>Four promised times present; one delivery time empty, allowed for an unfinished parcel</strong></dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this supports</strong> The checked input has no duplicate delivery identifiers or missing promised times. Its version and cutoff identify the records covered.</p>
<p class="evidence-limit"><strong>What it does not establish</strong> These checks establish neither the accuracy of the times nor delivery by the contract deadline. They also do not show that the measure answers the meeting's question or that the report read this input. A correctly calculated 66.7% still uses the wrong denominator for that question.</p>

If a check fails, retain its result and input reference. The reporting engineer investigates and notifies both consuming teams; a corrected snapshot and a new check result should remain distinguishable from the failed ones.

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
- **Make suitability visible in discovery.** Show scope, responsibility, status and access conditions; popularity is not evidence of fitness.
- **Contracts state commitments; check results supply evidence.** Keep the rule version, input and check time. Passing checks does not establish fitness for every purpose.
- **Dependencies identify places to investigate.** Collection may miss consumers.
- **Leave an actionable decision.** Name the evidence gap, next action and owner.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=7&amp;record=quality-check"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Find the checked input, identifier rule and observed identifier count. Distinguish the recorded result from the rule’s expectation.</li>
<li>Select <strong>Decision</strong>. Read the chosen rule, current gap and next action with its owner.</li>
</ol>
<p><strong>Think about it:</strong> Do the passed checks make the meeting’s all-due publication ready to use?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>No. The review covers <code>decision-input-1300</code>: four rows and four distinct identifiers satisfy <code>delivery-ids-unique-v1</code>. That supports uniqueness for this input. The meeting chooses all-due, expecting 50.0%, but its decision still has no verified all-due publication attached. The reporting engineer must verify the calculation and attach the output identifier and report refresh evidence. Passing checks does not establish the denominator or delivery to the report.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
