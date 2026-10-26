# 5. When the records are unreliable

A catalogue can contain accurate observations and still give a misleading picture. A scan may cover only part of a database. An event may arrive twice, or after a newer event. Two sources may disagree. Readers need to see what the evidence supports and where the answer remains uncertain.

## Absence needs an explanation

Suppose yesterday's scan found `delivery_summary`, but today's scan does not report it. The table might have been deleted. The collector might also have lost permission to see it, scanned the wrong database, or stopped before reaching it.

A missing record therefore means “not observed in this collection” until there is stronger evidence. Retain the last successful observation and mark the table as unverified while checking the collection's scope, permissions and outcome. A confirmed deletion could come from a recorded drop operation, or a completed scan that was able and expected to see every table in that database.

Removing the catalogue entry immediately would erase useful evidence while suggesting a certainty the collector does not have. Keeping an entry forever as apparently current would also mislead. Its visible status should distinguish last seen, currently unverified and confirmed deleted.

## Separate an event from its arrival

A scheduler may resend a publication message if the catalogue does not acknowledge receiving it. Use the source name and a stable event identifier to recognise the repeated message. Matching text or timestamps alone cannot reliably establish that two messages report the same occurrence.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · One delayed event and one repeated delivery</figcaption>

These invented records concern production `delivery_summary` on 21 October 2026, a separate day from Chapter 3. All times are UTC. The scheduler gives each event a stable identifier. In this example, the summary table also has a version label naming the run that published it.

| Record | What the source reports | Received by catalogue |
|---|---|---|
| Scheduler event `E20` | Run `R1000` published `summary-R1000` at 10:00. | 10:01; repeated at 10:04. |
| Scheduler event `E19` | Run `R0950` failed at 09:50. | 10:06. |
| Database scan `S7` | At 10:03, the table's version label named `summary-R0940`. | 10:05. |

</figure>

Receiving `E20` twice does not mean two publications happened. Count the publication once; the two receipt times can still help diagnose why the message was repeated. By contrast, another scan of the same unchanged table would be a new observation: it establishes that the collector saw the same state again.

Event time is when the reported occurrence happened; received time is when the catalogue learned about it. `E19` arrives last but describes the earlier failure. Sorting by arrival and labelling the job “failed” would conceal the later reported success. Keep the run identities and both times so the earlier failure remains visible in its proper context.

The [CloudEvents specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#required-attributes) provides a concrete convention: source plus event ID identifies a distinct event, and a resent duplicate can retain that identity. A collector needs an equivalent agreement with its producer to apply this reasoning.

## Show conflicts without inventing a resolution

At 10:03, the table still names an older version, `summary-R0940`, even though the scheduler reports publishing `summary-R1000` at 10:00. The version label could be wrong; the scheduler could also have reported publication incorrectly. These records alone do not resolve the disagreement.

The catalogue should show both claims and flag the latest publication as disputed. Metadata has [provenance](03-following-lineage.md#provenance) too: keep who or what supplied each claim and when. An investigator can then inspect the job's write logs and saved output versions. If that investigation resolves the conflict, record the supporting evidence alongside the conclusion. Choosing whichever message arrived last would make the display simpler while discarding the reason to investigate.

## Core points

- **Missing from a scan does not necessarily mean deleted.** Check collection scope, permissions and outcome before drawing that conclusion.
- **A repeated message is not another event.** Use the source and a stable event identifier to recognise duplicates.
- **Arrival order is not event order.** Keep event and receipt times so delayed messages do not obscure what happened.
- **Preserve conflicting claims and show uncertainty.** Keep their sources and times, then record the evidence used to resolve the disagreement.
