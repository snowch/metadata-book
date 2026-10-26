"""Run a local, invented lineage incident using only in-memory SQLite."""

from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
DATE = "2026-10-19 "

SCHEMA = """
CREATE TABLE code_versions (
    code_version TEXT PRIMARY KEY NOT NULL,
    sql_text TEXT NOT NULL
);
CREATE TABLE snapshots (
    snapshot_id TEXT PRIMARY KEY NOT NULL,
    captured_at TEXT NOT NULL,
    row_count INTEGER NOT NULL CHECK (row_count >= 0)
);
CREATE TABLE snapshot_rows (
    snapshot_id TEXT NOT NULL REFERENCES snapshots(snapshot_id),
    delivery_id TEXT NOT NULL,
    promised_at TEXT NOT NULL,
    delivered_at TEXT,
    PRIMARY KEY (snapshot_id, delivery_id)
);
CREATE TABLE runs (
    run_id TEXT PRIMARY KEY NOT NULL,
    job_name TEXT NOT NULL,
    code_version TEXT NOT NULL REFERENCES code_versions(code_version),
    input_snapshot_id TEXT NOT NULL REFERENCES snapshots(snapshot_id),
    status TEXT NOT NULL CHECK (status IN ('running', 'success', 'failed')),
    finished_at TEXT,
    error TEXT
);
CREATE TABLE outputs (
    output_version TEXT PRIMARY KEY NOT NULL,
    run_id TEXT NOT NULL UNIQUE REFERENCES runs(run_id),
    completed INTEGER NOT NULL,
    on_time INTEGER,
    percentage REAL,
    published_at TEXT NOT NULL
);
CREATE TABLE current_output (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    output_version TEXT NOT NULL REFERENCES outputs(output_version)
);
CREATE TABLE report_refreshes (
    refresh_id TEXT PRIMARY KEY NOT NULL,
    report_name TEXT NOT NULL,
    refreshed_at TEXT NOT NULL,
    output_version TEXT NOT NULL REFERENCES outputs(output_version)
);
CREATE TABLE simulation_events (
    event_id TEXT PRIMARY KEY NOT NULL,
    occurred_at TEXT NOT NULL,
    detail TEXT NOT NULL
);
"""


def replay(db, snapshot_id, code_version="completed-v1"):
    """Execute retained SQL against a separate copy of the retained input rows."""
    code = db.execute(
        "SELECT sql_text FROM code_versions WHERE code_version = ?", (code_version,)
    ).fetchone()
    if code is None:
        raise ValueError(f"Code version {code_version!r} is unavailable: retained SQL is missing")
    snapshot = db.execute(
        "SELECT row_count FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)
    ).fetchone()
    if snapshot is None:
        raise ValueError(f"Snapshot {snapshot_id!r} is unavailable: capture record is missing")
    rows = db.execute(
        """SELECT delivery_id, promised_at, delivered_at FROM snapshot_rows
           WHERE snapshot_id = ? ORDER BY delivery_id""", (snapshot_id,)
    ).fetchall()
    if len(rows) != snapshot[0]:
        raise ValueError(f"Snapshot {snapshot_id!r} is incomplete: "
                         f"expected {snapshot[0]} rows, found {len(rows)}")
    scratch = sqlite3.connect(":memory:")
    try:
        scratch.execute("""CREATE TABLE deliveries (
            delivery_id TEXT PRIMARY KEY, promised_at TEXT NOT NULL, delivered_at TEXT
        )""")
        scratch.executemany("INSERT INTO deliveries VALUES (?, ?, ?)", rows)
        return scratch.execute(code[0]).fetchone()
    finally:
        scratch.close()


def publish(db, run_id, output_version, published_at, fail_before_pointer=False):
    """Publish the output and pointer together; injected failures roll both back."""
    code, snapshot = db.execute(
        "SELECT code_version, input_snapshot_id FROM runs WHERE run_id = ?", (run_id,)
    ).fetchone()
    completed, on_time, percentage = replay(db, snapshot, code)
    with db:
        db.execute("INSERT INTO outputs VALUES (?, ?, ?, ?, ?, ?)",
                   (output_version, run_id, completed, on_time, percentage, published_at))
        if fail_before_pointer:
            # A deliberate local fault, not an operating-system permission probe.
            raise PermissionError("injected fault: destination write permission denied")
        db.execute("""INSERT INTO current_output VALUES (1, ?)
                      ON CONFLICT(singleton) DO UPDATE
                      SET output_version = excluded.output_version""", (output_version,))
        db.execute("UPDATE runs SET status = 'success', finished_at = ? WHERE run_id = ?",
                   (published_at, run_id))


def capture_run(db, suffix, time):
    """Save all current delivery rows and register a run before publication."""
    with db:
        db.execute("INSERT INTO snapshots SELECT ?, ?, COUNT(*) FROM deliveries",
                   ("S" + suffix, DATE + time))
        db.execute("""INSERT INTO snapshot_rows
                      SELECT ?, delivery_id, promised_at, delivered_at FROM deliveries""",
                   ("S" + suffix,))
        db.execute("INSERT INTO runs VALUES (?, ?, ?, ?, 'running', NULL, NULL)",
                   ("R" + suffix, "build_delivery_summary", "completed-v1", "S" + suffix))


def refresh_report(db, suffix, time):
    with db:
        db.execute("""INSERT INTO report_refreshes
                      SELECT ?, 'Delivery performance', ?, output_version
                      FROM current_output WHERE singleton = 1""", ("F" + suffix, DATE + time))


def build_incident():
    """Return the complete incident, including immutable historical references."""
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript((HERE.parent / "deliveries.sql").read_text())
    db.executescript(SCHEMA)
    with db:
        db.execute("INSERT INTO code_versions VALUES (?, ?)",
                   ("completed-v1", (HERE / "completed-v1.sql").read_text()))
        db.execute("UPDATE deliveries SET delivered_at = NULL WHERE delivery_id = 'D102'")
    capture_run(db, "1205", "12:05")
    publish(db, "R1205", "summary-R1205", DATE + "12:05")

    with db:
        db.execute("UPDATE deliveries SET delivered_at = ? WHERE delivery_id = 'D102'",
                   (DATE + "12:20",))
    capture_run(db, "1230", "12:30")
    try:
        publish(db, "R1230", "summary-R1230", DATE + "12:30", fail_before_pointer=True)
    except PermissionError as error:
        with db:
            db.execute("UPDATE runs SET status = 'failed', finished_at = ?, error = ? "
                       "WHERE run_id = 'R1230'", (DATE + "12:30", str(error)))
            db.execute("INSERT INTO simulation_events VALUES (?, ?, ?)",
                       ("permission-denied", DATE + "12:30", str(error)))
    refresh_report(db, "1300", "13:00")

    with db:
        db.execute("INSERT INTO simulation_events VALUES (?, ?, ?)",
                   ("permission-restored", DATE + "13:05",
                    "simulated destination write permission restored; injection disabled"))
    capture_run(db, "1310", "13:10")
    publish(db, "R1310", "summary-R1310", DATE + "13:10")
    refresh_report(db, "1312", "13:12")
    return db


def main():
    db = build_incident()
    queries = [
        ("Runs", "SELECT run_id, code_version, input_snapshot_id, status, error FROM runs"),
        ("Published outputs", "SELECT * FROM outputs ORDER BY published_at"),
        ("Report refreshes", """SELECT f.refresh_id, f.refreshed_at, f.output_version,
                                      o.completed, o.on_time, o.percentage
                               FROM report_refreshes AS f
                               JOIN outputs AS o ON o.output_version = f.output_version
                               ORDER BY f.refreshed_at"""),
        ("Trace F1300", (HERE / "trace-report.sql").read_text()),
        ("Current output", "SELECT output_version FROM current_output"),
        ("Simulation events", "SELECT * FROM simulation_events ORDER BY occurred_at"),
    ]
    try:
        print("Local simulation; all timestamps are UTC. No scheduler, dbt or BI connection.")
        for title, sql in queries:
            print(f"\n{title}:")
            for row in db.execute(sql):
                print(row)
    finally:
        db.close()


if __name__ == "__main__":
    main()
