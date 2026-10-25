# 2. What a database already knows

A database keeps descriptions of its tables so it can run queries. Those records include column names, declared types and rules about allowed values. We can query them through the same interface used to read business data.

The examples use SQLite with the four deliveries from Chapter 1. The [source SQL](../examples/deliveries.sql) contains the setup and saved query. Every result needed to follow the explanation is shown here.

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

The names identify the fields, and `type` gives their declared type. Here `TEXT` means text. A `notnull` value of 1 forbids null, SQL's marker for a missing value; 0 allows it. `pk` identifies columns in the primary key, which uniquely identifies each row. Here only `delivery_id` belongs to that key; the other columns have `pk` set to zero.

This structure helps us read a query: `promised_at` and `delivered_at` are the available fields for comparing promised and actual times. But names, types and flags do not fully explain business meaning. Allowing a missing `delivered_at` value does not tell us whether it means awaiting delivery, a late update, or an unknown time. In this example we treat null as not yet recorded as completed.

Similarly, `promised_at` could record the initial estimate or the latest commitment to the customer. Renaming the column changes the table's structure, or **schema**. Changing which promise fills it changes its meaning, even if the name and type stay the same. A reader needs the business definition to interpret these values.

SQLite records table and view definitions in `sqlite_schema`; its [schema table documentation](https://sqlite.org/schematab.html) describes those records. The `table_xinfo` fields are documented in [SQLite's pragma reference](https://sqlite.org/pragma.html#pragma_table_xinfo). Other databases expose similar structural information through their own catalogues.

## Read the calculation

The `on_time_completed` view is a saved query. SQLite calculates its result from the underlying table whenever the view is read. The relevant filter is:

```sql
FROM deliveries
WHERE delivered_at IS NOT NULL
```

This excerpt removes rows without a delivery time before the calculation counts them. With our four records, three have a delivery time; two of those were delivered by their promise time. Reading the view gives:

<div class="query-result" markdown="1">

| completed | on_time | percentage |
|---:|---:|---:|
| 3 | 2 | 66.7 |

</div>

The view measures punctuality among completed deliveries. It answers the first question in Chapter 1's table, giving 66.7%. Delivery Operations chose the second question, counting all deliveries due, which gives 50.0%. This view therefore does not implement that team's definition. Database records let us inspect the calculation; they do not supply the business decision.

The on-time comparison uses timestamps stored as text in the same fixed UTC format, `YYYY-MM-DD HH:MM`. For these values, text order matches time order. This is an assumption of the example, not something the `TEXT` declaration enforces.

## Two jobs for a catalogue

The word **catalogue** covers different jobs. A database or query-engine catalogue helps software find and read data. SQLite's schema records serve this purpose. [Hive Metastore](https://hive.apache.org/development/designdocs/design/#metastore) also describes table schemas, partitions—groups such as one day's deliveries—storage locations and file formats. It connects table names to stored data, rather than simply listing files.

A **discovery and governance catalogue**, such as DataHub or OpenMetadata, helps people find, understand and manage data. It connects technical records with definitions, responsible teams and lineage. These roles overlap: a database catalogue can also hold comments or ownership information. The distinction is their main purpose, not a strict division between technical and business metadata.

[Chapter 4](04-collecting-metadata.md) shows how a discovery catalogue collects descriptions from other systems. Those descriptions are data in the catalogue and metadata about the source.

A collected definition should identify its source and when it was observed. If the database changes before the catalogue refreshes, the catalogue still describes the earlier version. Collecting metadata makes it easier to find, but keeping it current remains a separate task.

The view recalculates when read. A scheduled process that writes a summary table behaves differently: its stored output may remain visible after a later run fails. To explain that output, we need to connect it to a particular execution and its inputs, the subject of Chapter 3.

<details class="further-detail" markdown="1">
<summary>Further detail: the complete calculation</summary>

Here is the complete query behind `on_time_completed`:

```sql
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

`COUNT(*)` counts the filtered rows, and the conditional sum counts those on time. `NULLIF` turns a zero denominator into null, so an empty set has no percentage rather than a misleading zero. The complete setup is in the [source SQL](../examples/deliveries.sql).

</details>

<details class="further-detail" markdown="1">
<summary>Further detail: SQLite types and timestamps</summary>

SQLite has no dedicated date/time storage class. This example uses text, but other SQLite applications may use numeric representations. Mixing timestamp formats or time zones would invalidate the simple text comparison used here.

Ordinary SQLite tables use type affinity rather than strict type enforcement. SQLite also offers strict tables, but neither approach automatically establishes a timestamp's business meaning. The [datatype documentation](https://sqlite.org/datatype3.html) describes these rules.

</details>
