"""Check the book's worked database results with real SQLite."""

from pathlib import Path
from html import unescape
import importlib.util
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def verify_lineage():
    path = ROOT / "examples/lineage/simulate.py"
    spec = importlib.util.spec_from_file_location("lineage_simulation", path)
    simulation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simulation)
    publish = simulation.publish
    failure_pointers = []

    def observe_publication(db, *args, **kwargs):
        try:
            return publish(db, *args, **kwargs)
        except PermissionError:
            # Observe rollback at the failure, before any report or recovery runs.
            failure_pointers.append(db.execute(
                "SELECT output_version FROM current_output"
            ).fetchone())
            assert db.execute("SELECT * FROM outputs WHERE run_id = 'R1230'").fetchall() == []
            raise

    simulation.publish = observe_publication
    try:
        db = simulation.build_incident()
    finally:
        simulation.publish = publish
    try:
        assert failure_pointers == [("summary-R1205",)], failure_pointers
        assert db.execute("PRAGMA foreign_keys").fetchone() == (1,)
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("SELECT COUNT(*) FROM outputs").fetchone() == (2,)
        assert db.execute("SELECT * FROM outputs WHERE run_id = 'R1230'").fetchall() == []
        assert db.execute("SELECT status, error FROM runs WHERE run_id = 'R1230'").fetchone() == (
            "failed", "injected fault: destination write permission denied"
        )
        refreshes = db.execute("""
            SELECT f.refresh_id, f.output_version, o.completed, o.on_time, o.percentage
            FROM report_refreshes AS f
            JOIN outputs AS o ON o.output_version = f.output_version
            ORDER BY f.refreshed_at
        """).fetchall()
        assert refreshes == [
            ("F1300", "summary-R1205", 2, 2, 100.0),
            ("F1312", "summary-R1310", 3, 2, 66.7),
        ], refreshes
        assert db.execute("SELECT output_version FROM current_output").fetchone() == (
            "summary-R1310",
        )
        trace = db.execute((path.parent / "trace-report.sql").read_text()).fetchall()
        assert trace == [("R1205", "completed-v1", "S1205")], trace
        reference = (path.parent / "README.md").read_text()
        printed_query = re.findall(r"```sql\n(.*?)\n```", reference, re.S)[0]
        assert db.execute(printed_query).fetchall() == trace

        # Check the displayed evidence against actual simulation records.
        cards = []
        for chapter, expected_count in [("03-following-lineage.md", 3), ("04-outdated-reports.md", 1)]:
            chapter_cards = re.findall(
                r'<figure class="metadata-record" data-table="([a-z_]+)">(.*?)</figure>',
                (ROOT / "chapters" / chapter).read_text(), re.S,
            )
            assert len(chapter_cards) == expected_count, chapter
            cards.extend(chapter_cards)
        keys = {"report_refreshes": "refresh_id", "outputs": "output_version", "runs": "run_id"}
        for table, body in cards:
            pairs = re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", body, re.S)
            fields = {unescape(re.sub(r"<[^>]+>", "", key)).strip():
                      unescape(re.sub(r"<[^>]+>", "", value)).strip()
                      for key, value in pairs}
            key = keys[table]
            cursor = db.execute(f'SELECT * FROM "{table}" WHERE "{key}" = ?', (fields[key],))
            row = cursor.fetchone()
            assert row is not None, fields
            actual = dict(zip((column[0] for column in cursor.description), row))
            assert len(fields) >= 4, fields
            for field, value in fields.items():
                assert value == str(actual[field]), (table, field, value, actual[field])
        ages = db.execute("""
            SELECT f.refresh_id,
                   (strftime('%s', f.refreshed_at) - strftime('%s', o.published_at)) / 60
            FROM report_refreshes AS f
            JOIN outputs AS o ON o.output_version = f.output_version
            ORDER BY f.refreshed_at
        """).fetchall()
        assert ages == [("F1300", 55), ("F1312", 2)], ages
        for snapshot, expected in [("S1205", (2, 2, 100.0)), ("S1310", (3, 2, 66.7))]:
            assert simulation.replay(db, snapshot) == expected
            assert db.execute("SELECT COUNT(*) FROM snapshot_rows WHERE snapshot_id = ?",
                              (snapshot,)).fetchone() == (4,)
        assert db.execute("""SELECT delivered_at FROM snapshot_rows
                             WHERE snapshot_id = 'S1205' AND delivery_id = 'D102'""").fetchone() == (None,)
        assert db.execute("""SELECT delivery_id, promised_at, delivered_at FROM snapshot_rows
                             WHERE snapshot_id = 'S1310' ORDER BY delivery_id""").fetchall() == db.execute(
            "SELECT delivery_id, promised_at, delivered_at FROM deliveries ORDER BY delivery_id"
        ).fetchall()

        def expect_replay_error(snapshot, code, message):
            try:
                simulation.replay(db, snapshot, code)
            except ValueError as error:
                assert message in str(error), str(error)
            else:
                raise AssertionError(f"Replay accepted unavailable evidence: {snapshot}, {code}")

        expect_replay_error("missing-snapshot", "completed-v1", "capture record is missing")
        expect_replay_error("S1205", "missing-code", "retained SQL is missing")
        db.execute("SAVEPOINT evidence_checks")
        try:
            original_sql = db.execute(
                "SELECT sql_text FROM code_versions WHERE code_version = 'completed-v1'"
            ).fetchone()[0]
            db.execute("INSERT INTO code_versions VALUES (?, ?)", (
                "all-due-exercise", original_sql.replace("WHERE delivered_at IS NOT NULL", "")
            ))
            assert simulation.replay(db, "S1205", "all-due-exercise") == (4, 2, 50.0)
            db.execute("DELETE FROM snapshot_rows WHERE snapshot_id = 'S1205' AND delivery_id = 'D101'")
            expect_replay_error("S1205", "completed-v1", "expected 4 rows, found 3")
            db.execute("DELETE FROM snapshot_rows WHERE snapshot_id = 'S1205'")
            expect_replay_error("S1205", "completed-v1", "expected 4 rows, found 0")
            db.execute("INSERT INTO snapshots VALUES ('Sempty', '2026-10-19 13:20', 0)")
            assert simulation.replay(db, "Sempty") == (0, None, None)

            # Current definitions can change; replay must use the original run's SQL.
            db.execute("DROP VIEW on_time_completed")
            db.execute("CREATE VIEW on_time_completed AS SELECT 999, 999, 999.0")
            assert db.execute("SELECT * FROM on_time_completed").fetchone() == (999, 999, 999.0)
            code = db.execute("SELECT code_version FROM runs WHERE run_id = 'R1310'").fetchone()[0]
            assert simulation.replay(db, "S1310", code) == (3, 2, 66.7)
            assert db.execute("SELECT sql_text FROM code_versions WHERE code_version = ?",
                              (code,)).fetchone()[0] == (path.parent / "completed-v1.sql").read_text()
        finally:
            db.execute("ROLLBACK TO evidence_checks")
            db.execute("RELEASE evidence_checks")
        assert simulation.replay(db, "S1205") == (2, 2, 100.0)

    finally:
        db.close()
    print("Verified lineage: retained inputs/code, missing evidence rejected, failure rollback, "
          "historical 100.0%, recovered 66.7%.")


def verify():
    with sqlite3.connect(":memory:") as db:
        db.executescript((ROOT / "examples/deliveries.sql").read_text())
        objects = db.execute("""
            SELECT type, name FROM sqlite_schema
            WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'
            ORDER BY type, name
        """).fetchall()
        assert objects == [("table", "deliveries"), ("view", "on_time_completed")], objects
        columns = db.execute('''
            SELECT name, type, "notnull", pk
            FROM pragma_table_xinfo('deliveries') ORDER BY cid
        ''').fetchall()
        assert columns == [
            ("delivery_id", "TEXT", 1, 1),
            ("promised_at", "TEXT", 1, 0),
            ("delivered_at", "TEXT", 0, 0),
        ], columns
        current = db.execute("SELECT * FROM on_time_completed").fetchone()
        assert current == (3, 2, 66.7), current
        due = db.execute("""
            SELECT COUNT(*),
                   ROUND(100.0 * SUM(CASE WHEN delivered_at <= promised_at
                                         THEN 1 ELSE 0 END) / COUNT(*), 1)
            FROM deliveries
        """).fetchone()
        assert due == (4, 50.0), due
        db.execute("UPDATE deliveries SET delivered_at = NULL WHERE delivery_id = 'D102'")
        earlier = db.execute("SELECT * FROM on_time_completed").fetchone()
        assert earlier == (2, 2, 100.0), earlier
        db.execute("DELETE FROM deliveries")
        empty = db.execute("SELECT * FROM on_time_completed").fetchone()
        assert empty == (0, None, None), empty
    print(f"Verified with SQLite {sqlite3.sqlite_version}: schema, 66.7%, 50.0%, 100.0%, empty input.")
    verify_lineage()


if __name__ == "__main__":
    verify()
