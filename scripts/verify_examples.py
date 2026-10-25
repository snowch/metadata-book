"""Check the book's worked database results with real SQLite."""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    verify()
