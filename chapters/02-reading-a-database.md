# 2. What a database already knows

A database keeps descriptions of its tables so it can run queries. Those records include column names, declared types and rules about allowed values. We can query them through the same interface used to read business data.

The examples use SQLite, with the four deliveries from Chapter 1 stored in a table named `deliveries`. Each row represents one delivery. The [source SQL](../examples/deliveries.sql) contains the setup and saved query. Every result needed to follow the explanation is shown here.

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
- **`type`** — its declared data type; here, all three columns declare `TEXT`.
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

<div class="query-result" markdown="1">

| completed | on_time | percentage |
|---:|---:|---:|
| 3 | 2 | 66.7 |

</div>

The view measures punctuality among completed deliveries. It answers the first question in Chapter 1's table, giving 66.7%. Delivery Operations chose the second question, counting all deliveries due, which gives 50.0%. This view therefore does not implement that team's definition. Database records let us inspect the calculation; they do not supply the business decision.

The on-time comparison uses timestamps stored as text in the same fixed UTC format, `YYYY-MM-DD HH:MM`. For these values, text order matches time order. This is an assumption of the example, not something the `TEXT` declaration enforces.

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

A collected definition should identify its source and when it was observed. If the database changes before the catalogue refreshes, the catalogue still describes the earlier version. Collecting metadata makes it easier to find, but keeping it current remains a separate task.

The view recalculates when read. A scheduled process that writes a summary table behaves differently: its stored output may remain visible after a later run fails. To explain that output, we need to connect it to a particular execution and its inputs, the subject of Chapter 3.

## Core points

- **Database records describe structure.** Column names, declared types and constraints do not fully explain what values mean.
- **Meaning can change without a schema change.** Storing a revised promise instead of the original promise changes the measure even if the column's name and type stay the same.
- **Read the calculation to see what it counts.** The completed-delivery view excludes unfinished deliveries, so it cannot answer the all-due question.
- **Catalogues serve different purposes.** Database catalogues help software find and read data; discovery catalogues connect technical records with definitions, owners and lineage. These roles overlap.

<details class="further-detail" markdown="1">
<summary>Further detail: SQLite types and timestamps</summary>

SQLite has no dedicated date/time storage class. This example uses text, but other SQLite applications may use numeric representations. Mixing timestamp formats or time zones would invalidate the simple text comparison used here.

Ordinary SQLite tables use type affinity rather than strict type enforcement. SQLite also offers strict tables, but neither approach automatically establishes a timestamp's business meaning. The [datatype documentation](https://sqlite.org/datatype3.html) describes these rules.

</details>
