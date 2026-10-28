# 6. When the records are unreliable

A catalogue can contain accurate observations and still mislead. A scan may cover only part of a database. An event may arrive twice, or after a newer event. Two sources may disagree. What should the catalogue display when it cannot establish a single current answer?

## Absence needs an explanation

Suppose yesterday's scan found `delivery_summary`, but today's does not report it. The table might have been deleted. The collector might also have lost permission, scanned the wrong database, or stopped before reaching it.

The entry should retain its last successful observation and show **currently unverified: not observed in today's collection**. Check the scan's scope, permissions and outcome before changing that status. Evidence of deletion could come from a recorded drop operation, or a completed scan that was able and expected to see every table in the database and confirmed this one absent.

Removing the entry immediately would erase useful evidence; leaving it apparently current would also mislead. Distinguish when the table was last seen, whether it is currently unverified, and whether deletion has been confirmed.

## Separate an event from its arrival

These invented records concern `prod/parcels/delivery_summary` on **21 October 2026**, a separate day from Chapters 3–4. All times are UTC. The scheduler assigns stable event identifiers. The table has a version label naming its published output. The catalogue display below is illustrative.

| Source record | What it reports | Received by catalogue |
|---|---|---|
| Scheduler event `E20` | Run `R1000` published `summary-R1000` at 10:00. | 10:01; repeated at 10:04. |
| Scheduler event `E19` | Run `R0950` failed at 09:50. | 10:06. |
| Database scan `S7` | At 10:03, the table's version label named `summary-R0940`. | 10:05. |

A scheduler may resend a message if receipt is not acknowledged. The source plus stable event identifier lets the catalogue recognise the repeated `E20`. Matching text or timestamps alone cannot reliably establish identity. Another scan of the unchanged table would be a new observation: it establishes that the collector saw the same state again.

Event time describes when an occurrence happened; receipt time describes when the catalogue learned about it. Here, `E19` arrives last but reports an earlier failure. Its arrival cannot turn run `R1000` into a failure. These timestamps explain this example's chronology; timestamps alone need not establish a reliable order across different systems.

## Show the decision and its evidence

The scheduler reports a publication at 10:00, but the database observation three minutes later still names an older version. The catalogue can show that disagreement while keeping event history intelligible:

<figure class="metadata-record">
<figcaption><span class="record-kind">Catalogue entry · Publication evidence</span><span class="record-source">As received by 10:06 UTC</span></figcaption>
<dl>
<div><dt>Dataset identifier</dt><dd><code>prod/parcels/delivery_summary</code></dd></div>
<div class="record-focus"><dt>Current published version</dt><dd><strong>Disputed: <code>summary-R1000</code> reported by scheduler event <code>E20</code>; <code>summary-R0940</code> observed by database scan <code>S7</code>.</strong></dd></div>
<div><dt>Reported publications for E20</dt><dd>One; received twice, at 10:01 and 10:04.</dd></div>
<div><dt>Earlier run outcome</dt><dd><code>R0950</code> failed at 09:50, according to <code>E19</code>; retained as earlier history despite its 10:06 arrival.</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The repeated message counts as one reported publication. The delayed failure belongs to a different, earlier run. Neither decision resolves the disagreement about which output the table contains.</p>
<p class="evidence-limit"><strong>What remains uncertain</strong> The version label could be wrong; the scheduler could have reported publication incorrectly. These records do not establish which claim is correct.</p>

Metadata has [provenance](03-following-lineage.md#provenance) too. Keep each claim's source and times so an investigator can check write logs and saved output versions. If that investigation resolves the disagreement, record the supporting evidence alongside the conclusion. Choosing whichever message arrived last would discard the reason to investigate.

## Core points

- **Missing from a scan does not necessarily mean deleted.** Check collection scope, permissions and outcome.
- **A repeated message is not another event.** Use the source and a stable event identifier to recognise duplicates.
- **Arrival order is not event order.** Retain run identities, event times and receipt times.
- **Preserve conflicting claims and show uncertainty.** Record the evidence used to resolve the disagreement.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=6&amp;record=source-observation"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Find what the database scan actually claimed and compare <strong>Observed at</strong> with <strong>Collected at</strong>.</li>
<li>Open <strong>Collection run</strong>. Read its scope and evidence limit. Suppose tomorrow’s scan omits this dataset: list what you would investigate.</li>
</ol>
<p><strong>Think about it:</strong> Does this observation establish creation at 09:02, or would a later omission establish deletion?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>Neither follows. The scan saw <code>percentage</code> in <code>prod/parcels/delivery_summary</code> at 09:00 on 20 October; the catalogue received that observation two minutes later. Those times describe observation and receipt, not creation. A later omission needs investigation of scope, permissions and collection outcome. Keep the last observation visible and mark current status unverified until deletion has supporting evidence; this map supplies no later scan or deletion record.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
