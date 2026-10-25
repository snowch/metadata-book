# 4. Collecting metadata from several systems

The parcel company's database describes `deliveries`. Its scheduler records executions of `build_delivery_summary`. Service Analytics maintains the completed-delivery definition used by that job. A discovery catalogue brings those descriptions together so a reader can follow the connections established in Chapter 3.

Collecting them requires more than copying names. Each record must identify what it describes, where the description came from and when it was observed or reported.

## Identify the same thing consistently

Suppose both the production database and a testing database contain `delivery_summary`. Production serves the report; testing holds trial calculations. Joining records on the table name alone would mix their histories.

An identifier must distinguish those locations. In this company, `prod/parcels/delivery_summary` names the table in the production `parcels` database; `test/parcels/delivery_summary` names its test counterpart. These identifiers follow an agreed naming rule. If the company adds another database system, that rule must distinguish it too.

The scheduler's output reference and the database collector's record must identify the same production table. A collector is the process that reads descriptions from a source and sends them to the catalogue. If collectors use different names, record which names refer to the same table before connecting their records.

## Collect different kinds of evidence

If the company later stores delivery data in Hive, its metastore describes the tables and where their data lives. Tools such as [DataHub](https://docs.datahub.com/docs/generated/ingestion/sources/hive-metastore/) and [OpenMetadata](https://docs.open-metadata.org/latest/connectors/database/hive) can collect those descriptions. In the discovery catalogue, the company can link `deliveries` to the definition of “delivered” and the team responsible for it. Collecting the description does not copy the delivery rows or replace the metastore used to query them.

Different collection methods answer different questions. A scheduled schema scan reads database descriptions at intervals: tables, columns and saved query definitions. A run event reports something about a particular execution, such as its completion. A human definition records a decision about meaning.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Three records about one production summary</figcaption>

This invented collection takes place on 20 October 2026, after the incident in Chapter 3. All times are UTC. Each record explicitly refers to the production `delivery_summary`.

| Record | Claim | Timing evidence |
|---|---|---|
| Database scan | The summary has a `percentage` column. | Observed at 09:00; collected at 09:02. |
| Scheduler event | Run `R0905` published output version `summary-R0905`. | Completion occurred at 09:05; collected at 09:06. |
| Service Analytics definition | The percentage counts on-time deliveries among completed deliveries. | Definition revised at 08:30; collected at 09:07. |

</figure>

The scan establishes the column's presence at 09:00. It does not establish which run last wrote its values. The scheduler supplies publication evidence for a particular run. The definition explains the denominator but does not prove that the published calculation follows it. Together, they describe the table's structure, its publication and its intended meaning.

## Keep the source and its times

Keep three times separate to make collection delays visible:

- **Source time** — when the job finished or the definition was revised.
- **Observation time** — when a collector checked the source.
- **Collection time** — when the catalogue received the record.

For the schema scan, we know when the collector saw the column. We do not know when the column was created unless the database supplies that evidence. Recording 09:00 as its creation time would invent a fact.

<blockquote class="key-principle" markdown="1">

**Connect collected records by identity, while preserving what each source actually establishes.**

</blockquote>

Collection also does not appoint an owner. Service Analytics must accept responsibility for this definition; the catalogue can record that agreement. Importing the description does not make the person running the collector responsible for what the metric means.

The catalogue now connects descriptions of the summary, its publication and its intended meaning. Next we need to decide how to present this evidence when collection is incomplete or records disagree.

<details class="further-detail" markdown="1">
<summary>Further detail: identifiers in OpenLineage</summary>

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) identifies a dataset using a namespace and name. The namespace distinguishes the system containing the dataset; the name identifies it within that system. Collectors must agree on both for their records to connect. Matching the short table name alone is insufficient.

</details>
