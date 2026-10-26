# A local lineage incident

For a guided investigation, read the optional [practical walkthrough](walkthrough.md). This page describes the simulation and its records. [Chapter 3](../../chapters/03-following-lineage.md) teaches the core ideas without requiring execution.

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

Foreign keys connect the records. [trace-report.sql](trace-report.sql) follows F1300 to its producer and returns:

```text
run_id  code_version  input_snapshot_id
R1205   completed-v1  S1205
```

This is a local simulation, not evidence captured from a live scheduler, dbt deployment, database service or BI report. Its explicit snapshot copies and report refresh references stand in for integration work a real system would need. The permission error is a deliberately injected, known cause; a failed run status by itself would not reveal that cause. The 13:05 event changes which simulated fault is requested, not a filesystem permission.
