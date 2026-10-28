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
