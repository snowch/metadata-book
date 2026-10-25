# 3. Following a number to its source

The SQLite view `on_time_completed` calculates its result whenever it is queried. Now suppose the parcel company uses a scheduled transformation to write a stored table, `delivery_summary`, which the report **Delivery performance** reads. At 13:00 UTC on 19 October 2026, the report shows 100%, while the current on-time rate among completed deliveries is 66.7%. Both use the completed-delivery denominator. We need to establish which records produced the displayed number.

Lineage describes the relationships through which data is produced and transformed. It connects an output to its inputs and processing steps, giving us a route to investigate.

## Follow the value through the incident

At the observation time, `deliveries` contains four rows, all times UTC:

| Delivery | Promised | Delivered |
|---|---:|---:|
| D101 | 12:00 | 11:50 |
| D102 | 12:00 | 12:20 |
| D103 | 12:00 | 11:40 |
| D104 | 12:00 | NULL |

D104 is unfinished. Among the three completed deliveries, D101 and D103 were on time, so the current rate is 2/3, or 66.7%. The lineage path is:

`deliveries` → `build_delivery_summary` → `delivery_summary` → **Delivery performance**

Suppose the on-call engineer finds a successful transformation run at 12:05 and a failed attempt at 12:30. Merely seeing a 100% value and those two events does not identify the report’s data. The value could be cached, or the report might read a different table. The source’s current rows also cannot establish which snapshot an earlier run read. To connect the number to its origin, gather the run’s input and output evidence, publication history, and the report’s refresh record.

The following records are illustrative, invented for this chapter, and were not captured from deployed tools:

| Record | Time and status | Evidence |
|---|---|---|
| Run R-1205 | 12:05, succeeded | Read a `deliveries` snapshot containing all four IDs; D101 and D103 had delivery times, while D102 and D104 had `delivered_at = NULL`. Published version `summary-R1205`: completed 2, on time 2, rate 100%. |
| Run R-1230 | 12:30, failed before publication | No output published; the previous successful output remained available. |
| Report refresh | 13:00 | **Delivery performance** read `summary-R1205`. |

These records make the evidence chain explicit. R-1205 saw only two completed parcels, both on time, and published 2/2 = 100%. D102 was delivered at 12:20, after that captured snapshot. With the 13:00 source state, the same completed-only rule gives 2/3 = 66.7%. The report refresh record ties its displayed 100% to the older output version.

The supported diagnosis is that the report served a stale successful publication. R-1230 is consistent with why a newer result was not published, since the attempt failed before publication and the old output remained available. The failed attempt alone would not prove that the report read old data or explain why; the publication and refresh records establish that connection. In a live investigation, inspect the report’s cache or extract configuration too, especially if its refresh record does not identify the exact table version it read.

This stored table behaves differently from the earlier SQLite view. A view evaluates its query when read, so a newly delivered parcel can affect the next query. The scheduled transformation writes a result at a point in time; it stays at that version until a later successful publication replaces it. This distinction helps explain why an up-to-date source can coexist with an old report.

## Read declared lineage and runtime records

The graph above is a map of the route to investigate. A declared dependency graph records project structure, while runtime evidence records what happened during an execution. They answer related but separate questions.

dbt is a tool for building and managing data transformations. A dbt model commonly defines a transformation as a SQL query. Its `manifest.json` file describes models and other project resources; `parent_map` and `child_map` record their immediate dependencies. These relationships help identify likely downstream consumers. They do not establish that a particular run executed every model or read a particular physical snapshot. The [dbt manifest reference](https://docs.getdbt.com/reference/artifacts/manifest-json) describes the file's contents.

`run_results.json` records timing and status information for resources in a dbt invocation. Results can include skipped resources, so inspect the status before concluding that a model executed. The file does not provide a complete observed input-dataset list for each model and cannot, on its own, substantiate the captured-input claim in our incident. See [dbt's run results reference](https://docs.getdbt.com/reference/artifacts/run-results-json) and its [status schema](https://schemas.getdbt.com/dbt/run-results/v6.json).

OpenLineage is an open standard for exchanging lineage information. Integrations in processing tools can emit a `RunEvent` identifying a job, its run, state, and input and output datasets. What arrives depends on the integration: an event may report only some of a run's inputs, with other inputs reported later. The consumer must combine the events for that run where this reporting pattern is used. Dataset names alone still do not identify the exact rows read. See the [OpenLineage object model](https://openlineage.io/docs/spec/object-model/) and [run cycle](https://openlineage.io/docs/spec/run-cycle/).

## Trace meaning and possible impact

Lineage can show which transformation produced a table and which reports may depend on it. It cannot decide whether an unfinished parcel belongs in a denominator, what time zone defines “on time,” or whether a late correction should change a prior report. Those are semantic rules. Validate the SQL or transformation logic and the report’s metric definition against the stated cutoff and current source records.

Column-level lineage can make the route more precise. It may map an output such as `on_time_count` to source columns and expressions, narrowing where to look when logic changes. It also supports impact analysis: changing `promised_at` may affect this metric, while changing an unrelated address note may not. That map identifies potential downstream impact; it does not confirm a consumer failure. To establish an actual failure, inspect the consumer’s query, refresh, or displayed result.

For a useful record, keep run identity, times, status, code version, reported input datasets and snapshot identifiers, output version, and publication outcome together. Where a report reads a stored result, record the version or refresh reference as well. A timestamp without a run identifier is difficult to join reliably to a job log; a run identifier without input and output references says little about the value. These records make an account of the number possible while preserving the distinction between declared relationships, observed execution, and metric meaning.
