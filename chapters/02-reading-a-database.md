# 2. What a database already knows

A database keeps descriptions of its tables so it can run queries. Those records include column names, declared types and rules about allowed values. We can query them through the same interface used to read business data.

The examples use SQLite, with the four deliveries from Chapter 1 stored in a table named `deliveries`. Each row represents one delivery. The [source SQL](../examples/deliveries.sql) contains the setup and saved query. Every result needed to follow the explanation is shown here.

<figure class="chapter-video" aria-labelledby="chapter-video-title">
<figcaption id="chapter-video-title"><span>Watch the chapter</span><span class="chapter-video-duration">3 min 52 sec</span></figcaption>
<video controls playsinline preload="none" width="1280" height="720" poster="../assets/video/chapter-02/poster.jpg" aria-label="What a database already knows: narrated Chapter 2 explainer" aria-describedby="chapter-video-note">
<source src="../assets/video/chapter-02/chapter-02.mp4" type="video/mp4">
<track kind="captions" src="../assets/video/chapter-02/captions.vtt" srclang="en" label="English">
Your browser cannot play this video. <a href="../assets/video/chapter-02/chapter-02.mp4">Download the video</a> or <a href="../assets/video/chapter-02/transcript.txt">read the transcript</a>.
</video>
<p class="chapter-video-note" id="chapter-video-note">The delivery example is invented and assumes complete records at the measurement time. Narration uses a synthetic voice.</p>
<p class="chapter-video-links"><a href="../assets/video/chapter-02/transcript.txt">Read the transcript</a><a href="../assets/video/chapter-02/chapter-02.mp4" download>Download video <span>(6 MB)</span></a></p>
</figure>

## Inspect the columns

In SQLite, querying `pragma_table_xinfo('deliveries')` returns one row for each column in `deliveries`. We select four fields and sort the rows into column order:

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Inspecting the deliveries table</figcaption>

```sql
SELECT name, type, "notnull", pk
FROM pragma_table_xinfo('deliveries')
ORDER BY cid;
```

| name | type | notnull | pk |
|---|---|---:|---:|
| delivery_id | TEXT | 1 | 1 |
| promised_at | TEXT | 1 | 0 |
| delivered_at | TEXT | 0 | 0 |

</figure>

Read the four fields as follows:

- **`name`** — the column's name.
- **`type`** — its declared data type; here, all three columns declare `TEXT`. In this SQLite table, the declaration does not strictly enforce the type of every stored value.
- **`notnull`** — `1` means a value is required; `0` allows `NULL`, SQL's marker for a missing value.
- **`pk`** — the column's position in the primary key, which uniquely identifies each row. Here, `delivery_id` is the only key column (`1`); the others are not part of the key (`0`).

The column list shows which fields a query can use, but not exactly what their values mean. Allowing a missing `delivered_at` value does not tell us whether it means awaiting delivery, a late update, or an unknown time. In our four-row example, `NULL` means the parcel has not yet been delivered.

Suppose a customer was promised delivery by noon, then given a revised time of 12:30. A parcel arriving at 12:20 is late against the original promise but on time against the revised one. We need to know which promise `promised_at` stores—the column name alone cannot tell us.

Renaming a column changes the table's structure, or **schema**. Switching from storing the original promise to storing the revised promise changes what the column means, even if its name and type stay the same.

SQLite records table and view definitions in `sqlite_schema`; its [schema table documentation](https://sqlite.org/schematab.html) describes those records. The `table_xinfo` fields are documented in [SQLite's pragma reference](https://sqlite.org/pragma.html#pragma_table_xinfo). Other databases expose similar structural information through their own catalogues.

## Read the calculation

A view is a named query that you can read like a table. SQLite calculates its result from `deliveries` whenever the view is read. Here is the complete definition of `on_time_completed`:

```sql
CREATE VIEW on_time_completed AS
SELECT
    COUNT(*) AS completed,
    SUM(CASE WHEN delivered_at <= promised_at THEN 1 ELSE 0 END) AS on_time,
    ROUND(
        100.0 * SUM(CASE WHEN delivered_at <= promised_at THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS percentage
FROM deliveries
WHERE delivered_at IS NOT NULL;
```

The **`WHERE delivered_at IS NOT NULL`** filter excludes unfinished deliveries. `COUNT(*)` counts the three remaining rows; the `SUM(CASE ...)` expression counts the two that arrived on time. The percentage is two out of three, rounded to one decimal place. `NULLIF` makes the percentage `NULL` if there are no completed deliveries.

Read the view with:

```sql
SELECT * FROM on_time_completed;
```

<figure class="worked-example query-result" markdown="1">
<figcaption>Calculated output · Completed-delivery view</figcaption>

| completed | on_time | percentage |
|---:|---:|---:|
| 3 | 2 | **66.7** |

</figure>

<p class="evidence-reading"><strong>What this tells us</strong> The view counts three completed deliveries and returns 66.7%. Delivery Operations needs all four deliveries due to be counted, giving 50.0%. This view does not implement that team’s definition.</p>

The saved query is metadata describing a calculation; the returned percentage is its output data. Inspecting the query reveals what it counts, but does not establish which rule the business needs.

The on-time comparison uses timestamps stored as text in the same fixed UTC format, `YYYY-MM-DD HH:MM`. For these values, text order matches time order. This is an assumption of the example, not something the `TEXT` declaration enforces. The [SQLite implementation notes](../examples/README.md#sqlite-types-and-timestamps) explain the storage choices.

## Two jobs for a catalogue

The word **catalogue** covers different jobs.

<div class="definition-box" markdown="1">

**Database or query-engine catalogue**

Helps software find and read data. SQLite's schema records serve this purpose. [Hive Metastore](https://hive.apache.org/development/designdocs/design/#metastore) also describes table schemas, partitions—groups such as one day's deliveries—storage locations and file formats. It connects table names to stored data, rather than simply listing files.

</div>

<div class="definition-box" markdown="1">

**Discovery and governance catalogue**

Helps people find, understand and manage data. Tools such as DataHub and OpenMetadata connect technical records with definitions, responsible teams and lineage.

</div>

These roles overlap: a database catalogue can also hold comments or ownership information. The distinction is their main purpose, not a strict division between technical and business metadata.

[Chapter 5](05-collecting-metadata.md) shows how a discovery catalogue collects descriptions from other systems. Those descriptions are data in the catalogue and metadata about the source.

This view recalculates when read. [Chapter 3](03-following-lineage.md) follows a report that reads a stored result, connecting it to the execution and inputs that produced it.

## Core points

- **Database records describe structure.** Column names, declared types and constraints do not fully explain what values mean.
- **Meaning can change without a schema change.** Storing a revised promise instead of the original promise changes the measure even if the column's name and type stay the same.
- **Read the calculation to see what it counts.** The completed-delivery view excludes unfinished deliveries, so it cannot answer the all-due question.
- **Catalogues serve different purposes.** Database catalogues help software find and read data; discovery catalogues connect technical records with definitions, owners and lineage. These roles overlap.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=2&amp;record=column"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Find <code>delivered_at</code>’s declared type and <code>notnull</code> value. What does the database permit?</li>
<li>Select <strong>Saved query</strong>. Compare its filter and denominator with <strong>Metric definition</strong>.</li>
</ol>
<p><strong>Think about it:</strong> Can the saved query implement the all-due definition, and does the column declaration explain a missing delivery time?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p><code>TEXT</code> declares a text field; <code>notnull: 0</code> allows <code>NULL</code>, SQL’s marker for a missing value. They do not explain its meaning. The saved query filters out those rows with <code>delivered_at IS NOT NULL</code> and counts completed deliveries; the all-due definition includes unfinished parcels. The schema describes allowed structure; the filter reveals the calculation’s narrower population.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
