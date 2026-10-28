# 5. Collecting metadata from several systems

The database describes the parcel company's tables. Its scheduler records executions of `build_delivery_summary`. Service Analytics maintains the definition used by that job. How can a discovery catalogue bring those descriptions together without confusing what each source establishes?

## Identify the same thing consistently

Production and testing both contain a table called `delivery_summary`. The catalogue uses agreed identifiers to keep them apart:

| Catalogue identifier | What it identifies |
|---|---|
| `prod/parcels/delivery_summary` | The production table serving the report. |
| `test/parcels/delivery_summary` | A test table holding trial calculations. |

The naming rule distinguishes the environment, database and table. It must also distinguish database systems if the company adds another. A **collector** reads descriptions from a source and sends them to the catalogue. The scheduler's output reference and the database collector must resolve to the same production identifier. Where sources use different names, record their correspondence before joining their claims.

A name is not a permanent identity. Renaming `delivery_summary` may preserve the same dataset; dropping it and creating an unrelated table under that name does not. Keep a source identifier or recorded change history where available, and check that this is still the same dataset before reusing its definitions or lineage. Otherwise, old explanations can become attached to new data merely because the name matches.

## Read the assembled entry

This catalogue entry combines three invented records on **20 October 2026**. All times are UTC. The layout is illustrative; field names vary by tool.

<figure class="metadata-record">
<figcaption><span class="record-kind">Catalogue entry · Production summary</span><span class="record-source">Database scan, scheduler and Service Analytics</span></figcaption>
<dl>
<div class="record-focus"><dt>Dataset identifier</dt><dd><strong><code>prod/parcels/delivery_summary</code></strong></dd></div>
<div><dt>Structure</dt><dd>Column <code>percentage</code> exists.<br>Source: production database scan; observed 09:00, collected 09:02.</dd></div>
<div class="record-focus"><dt>Reported publication</dt><dd><strong>Run <code>R0905</code> published version <code>summary-R0905</code> to this dataset.</strong><br>Source: scheduler; completion occurred 09:05, collected 09:06.</dd></div>
<div><dt>Intended meaning</dt><dd>Percentage of completed deliveries that arrived on time.<br>Source: Service Analytics definition; revised 08:30, collected 09:07.</dd></div>
<div><dt>Responsibility for definition</dt><dd>Service Analytics; accepted in its definition record.</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The shared dataset identifier connects structure, a reported publication and intended meaning. <code>summary-R0905</code> identifies a particular output version; it does not replace the identifier for the table that receives successive versions.</p>
<p class="evidence-limit"><strong>What it does not tell us</strong> The scan does not identify the run that wrote the values. The definition explains the denominator but does not prove that the published calculation follows it. That requires the run's inputs and code, as shown in Chapter 3.</p>

The entry preserves separate claims instead of treating whichever source arrived last as an authority for everything. It also records an accepted responsibility: importing a team name alone would not establish that agreement or make the collector's operator responsible for the metric's meaning.

## Keep the source and its times

The display distinguishes three kinds of time:

- **Source time** — when the job finished or the definition was revised.
- **Observation time** — when a collector checked the source.
- **Collection time** — when the catalogue received the record.

The 09:00 scan establishes when the collector saw the column. Its creation time remains unknown unless the database supplies that evidence. Calling 09:00 its creation time would invent a fact. The scheduler's one-minute collection delay likewise changes when the catalogue learned of completion, not when completion occurred.

If the company later stores delivery data in Hive, its metastore describes tables and their data locations. [DataHub](https://docs.datahub.com/docs/generated/ingestion/sources/hive-metastore/) and [OpenMetadata](https://docs.open-metadata.org/latest/connectors/database/hive) offer collectors for those descriptions. Collecting them does not copy delivery rows or replace the metastore used to query them. A scheduled schema scan can describe columns and saved query definitions; execution evidence still comes from the scheduler or processing job, and meaning from the agreed definition.

## Core points

- **Connect records using agreed identifiers.** Distinguish production from testing, and a dataset from its output versions.
- **Each source establishes different facts.** Structure, execution and intended meaning need their own evidence.
- **Keep sources and times visible.** Occurrence, observation and collection may happen at different times.
- **Collection does not assign responsibility.** Record the responsible team's agreement.
