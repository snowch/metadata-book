# 2. What a database already knows

A database needs a description of its tables before it can execute a query. It must know which columns exist, how values are stored, and which constraints to apply. That description is already a useful source of metadata. We can inspect it using the same SQL interface we use to read business data.

SQLite makes this easy to see in a small example. The queries below operate on an actual SQLite database containing the four deliveries from Chapter 1. Their results are shown alongside them. You can follow the explanation without running anything; the [source SQL](../examples/deliveries.sql) is available if you want to reproduce it.

## Find the objects

Our example database has a table named `deliveries` and a view named `on_time_completed`. A view is a saved query: reading this view calculates a result from the underlying table. It does not keep a separately refreshed copy of that result.

SQLite records definitions of tables, views, indexes and triggers in `sqlite_schema`. This query selects the user-facing tables and views:

```sql
SELECT type, name
FROM sqlite_schema
WHERE type IN ('table', 'view')
  AND name NOT LIKE 'sqlite_%'
ORDER BY type, name;
```

| type | name |
|---|---|
| table | deliveries |
| view | on_time_completed |

The result is an inventory, rather than a sample of deliveries. It answers what is defined in this database. It does not establish whether anyone still uses the view, which report consumes it, or who should approve a change to it. Those questions require additional records.

The object definitions are also available in the `sql` column of `sqlite_schema`. For example, selecting the definition of `deliveries` shows the structure created by this statement:

```sql
CREATE TABLE deliveries (
    delivery_id TEXT PRIMARY KEY NOT NULL,
    promised_at TEXT NOT NULL,
    delivered_at TEXT
);
```

SQLite maintains these definitions as the schema changes. The database's own [schema table documentation](https://sqlite.org/schematab.html) explains the objects and fields it records. A catalogue collecting structural metadata can query this source instead of asking someone to retype column names into a spreadsheet.

## Inspect the columns

For a structured description of a table's columns, SQLite provides `table_xinfo`. Its table-valued form lets us select the fields we need:

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

Here `notnull = 1` means the column has a non-null constraint. The `pk` value gives its position in the primary key, or zero when it is not part of that key. Our key has one column, `delivery_id`. These are properties of the table definition, so they hold independently of the particular four rows we inserted.

The nullable `delivered_at` column allows D104's missing delivery time. That permission does not explain the missing value. The business system might use null for a parcel awaiting delivery, an event not yet received, or an unknown time. Our example assumes the snapshot is complete and uses null for a delivery not yet recorded as completed. A production description should identify the intended meaning and how delayed updates are handled.

The function and its result fields are documented in [SQLite's `table_xinfo` reference](https://sqlite.org/pragma.html#pragma_table_xinfo). This interface is specific to SQLite; another database may expose similar information through different catalogue tables or views. The general method transfers: inspect the database's records of its own structure.

## A declared type has limits

Both time columns are declared `TEXT`. SQLite has no dedicated date/time storage class, so this example stores UTC timestamps in a consistent `YYYY-MM-DD HH:MM` format. For these values, text ordering gives the same ordering as time. Mixing time zones or inconsistent date formats would invalidate that assumption.

The table definition does not validate the timestamp format. It also says nothing about whether a promise means the initial estimate or the latest commitment to the customer. Renaming the column changes the schema. Recording the latest commitment instead of the initial estimate changes its meaning, even if its name and type stay the same.

SQLite's ordinary tables use type affinity rather than the strict typing many readers expect from other databases. A declaration should therefore be interpreted according to the database's actual rules. SQLite also offers strict tables, but they would not, by themselves, define the business meaning of these timestamps. The [datatype documentation](https://sqlite.org/datatype3.html) describes these distinctions.

A useful catalogue should preserve the declared type and identify the source system. Replacing every database-specific type with a broad label such as “date” can discard information a reader needs to assess a query.

## Read the calculation

The view's definition exposes another kind of metadata: the transformation that produces a result. Its query is:

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

The `WHERE` clause removes deliveries without a completion time before the counts are calculated. `COUNT(*)` therefore counts completed deliveries. The conditional sum counts those completed at or before their promised times. Multiplication by `100.0` gives a percentage; `NULLIF` makes the denominator null when there are no completed deliveries, so the result is undefined rather than a misleading zero per cent.

Querying the view gives:

```sql
SELECT * FROM on_time_completed;
```

| completed | on_time | percentage |
|---:|---:|---:|
| 3 | 2 | 66.7 |

This explains what the implementation calculates. It counts punctuality among completed deliveries. A report intended to show the proportion of all due deliveries completed on time would need the other denominator from Chapter 1. The query and the agreed definition can now be compared directly.

The same query also reveals a dependency: it reads `deliveries`, specifically the two time columns. Renaming `promised_at` would require reviewing this definition. The database's object list alone did not show that relationship; reading the view's SQL exposed it.

## Collecting metadata creates another copy

A catalogue could periodically collect the object inventory, columns and view definitions. That would make them searchable alongside metadata from other systems. It could also associate `deliveries` with Delivery Operations and link the view to an agreed metric definition. The descriptions are data for the catalogue and metadata about the source tables.

Each collected description needs enough context to locate its source. A table name alone is ambiguous if development and production both contain `deliveries`. A source identifier, database and object name distinguish those assets. The collection time then tells a reader when the catalogue last checked the database.

Suppose a developer changes the view after collection. The database has the new definition; the catalogue still holds the earlier one until it collects again. Searching the catalogue is useful, but its answer now describes an earlier observation. Retaining that earlier definition may help an investigation, provided its observation time remains attached.

The view itself recalculates when queried. A scheduled process that writes a summary table has different behaviour: its previous output can remain visible after a later attempt fails. To explain a number read from that table, we need to connect the output to a particular execution and its inputs.
