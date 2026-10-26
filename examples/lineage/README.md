# A local lineage incident

For the evidence and its interpretation, read [Chapter 3: Where did this number come from?](../../chapters/03-following-lineage.md) and [Chapter 4: Why is this report out of date?](../../chapters/04-outdated-reports.md). Both show the records inline without requiring execution. This supporting reference describes the simulation and its records.

To reproduce the invented incident, use Python 3 from the repository root:

```sh
python3 examples/lineage/simulate.py
python3 scripts/verify_examples.py
```

Both commands use only Python's standard library and SQLite in memory. They create no persistent database and make no network calls. All timestamps are UTC on 19 October 2026.

The simulation retains the same four invented parcels as `examples/deliveries.sql`. At 12:05 D102 has no recorded completion; at 12:20 it gains its late completion. D104 remains uncompleted. The retained [completed-v1.sql](completed-v1.sql) executes the same calculation as the original view. Each run reads a saved copy of all four input rows, and `replay()` executes the retained SQL on a fresh copy of those rows. It raises `ValueError` if the code or capture record is missing, or if the retained row count differs from the count recorded at capture. A recorded zero-row snapshot remains a valid empty input. This count check detects missing rows; it does not detect changes that preserve the count.

| Record | Result |
|---|---|
| R1205, using S1205 | Publishes summary-R1205: 2 completed, 2 on time, 100.0%. |
| R1230, using S1230 | An injected `PermissionError` rolls back publication; summary-R1205 remains current. |
| F1300 | Reads summary-R1205 and therefore displays 100.0%. |
| 13:05 recovery event | Simulates restoring destination write permission by disabling the injected fault. |
| R1310, using S1310 | Same source rows as at 13:00 and same code; publishes summary-R1310: 3 completed, 2 on time, 66.7%. |
| F1312 | Reads summary-R1310 and therefore displays 66.7%. |

Outputs and report refreshes are separate historical rows. A successful publication inserts an output, changes the current pointer, and marks the run successful in one transaction. The failure occurs after inserting an output but before updating the pointer, so rollback removes the partial output. Recovery adds new history without replacing the earlier output or refresh.

## Retained records

`build_incident()` returns an open `sqlite3.Connection`; the caller closes it. Its tables are:

| Table | Purpose |
|---|---|
| `deliveries` | Current source rows, with the original `on_time_completed` view. |
| `code_versions(code_version, sql_text)` | The actual SQL text executed. |
| `snapshots(snapshot_id, captured_at, row_count)` | Capture times and original row counts for S1205, S1230 and S1310. |
| `snapshot_rows(snapshot_id, delivery_id, promised_at, delivered_at)` | The four rows read by each run. |
| `runs(run_id, job_name, code_version, input_snapshot_id, status, finished_at, error)` | Execution identity and outcome. |
| `outputs(output_version, run_id, completed, on_time, percentage, published_at)` | Successfully published versions. |
| `current_output(singleton, output_version)` | The currently published version, in the single row with key 1. |
| `report_refreshes(refresh_id, report_name, refreshed_at, output_version)` | The output version read by each report refresh. |
| `simulation_events(event_id, occurred_at, detail)` | The known injected permission fault and simulated restoration. |

Foreign keys connect the records. [trace-report.sql](trace-report.sql) follows F1300 to its producer:

```sql
SELECT r.run_id, r.code_version, r.input_snapshot_id
FROM report_refreshes AS f
JOIN outputs AS o ON o.output_version = f.output_version
JOIN runs AS r ON r.run_id = o.run_id
WHERE f.refresh_id = 'F1300';
```

It returns:

```text
run_id  code_version  input_snapshot_id
R1205   completed-v1  S1205
```

This is a local simulation, not evidence captured from a live scheduler, dbt deployment, database service or BI report. Its explicit snapshot copies and report refresh references stand in for integration work a real system would need. The permission error is a deliberately injected, known cause; a failed run status by itself would not reveal that cause. The 13:05 event changes which simulated fault is requested, not a filesystem permission.

## Decide how much history to keep

Saving four rows is cheap. Copying a large input for every run may be expensive. Where the storage system already retains immutable versions, a run can reference the version it read instead of creating another full copy. That only works while the referenced data remains available.

Suppose this team must investigate reports for 30 days. It could agree to keep input versions for 35 days, allowing five days for investigations opened near the deadline. Run records, code versions, outputs and report refreshes must remain available for at least the same investigations. These periods are a policy for this example, not a universal recommendation.

For example, retaining a separate 10 GB input copy every hour for 35 days requires **8.4 TB** before compression: 10 × 24 × 35 = 8,400 GB. Shared immutable versions may reduce that storage, but their expiry still limits replay. Metadata events also accumulate as runs and report refreshes increase.

Set an expiry policy and check that cleanup does not remove evidence still needed for an open investigation. Retained data needs appropriate access controls too.

After an input expires, the catalogue may still show which run and output a report used. It can no longer support replaying or independently checking that calculation from the original rows. Mark that limit explicitly: a saved identifier is not the same as saved evidence. The simulator refuses to replay a snapshot if its retained row count is incomplete; missing evidence is not an empty input.

<details class="further-detail" markdown="1">
<summary>Further detail: records from dbt and OpenLineage</summary>

dbt runs SQL queries to build tables and views. Its [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json) describes these planned steps; `parent_map` and `child_map` record their immediate dependencies. Its [run results file](https://docs.getdbt.com/reference/artifacts/run-results-json) records statuses and timings. The [status schema](https://schemas.getdbt.com/dbt/run-results/v6.json) includes skipped steps, so appearing in this file does not prove a query ran. It does not supply a complete list of the inputs actually read by each query.

OpenLineage is an open standard for exchanging lineage records. A processing tool can send a `RunEvent` identifying a job, run, state and reported input and output datasets. Some tools report additional inputs in later events, so readers must combine events for the same run. Dataset names alone do not preserve the rows read. See the [object model](https://openlineage.io/docs/spec/object-model/) and [run cycle](https://openlineage.io/docs/spec/run-cycle/).

Useful retained fields include run identity, times, status, code version, input snapshot references, output version, publication outcome and report refresh reference. Their availability depends on the tools and retention arrangements; a lineage event alone does not guarantee them.

</details>
