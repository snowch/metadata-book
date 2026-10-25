-- Invented snapshot: 19 October 2026, 13:00 UTC.
-- All timestamps use YYYY-MM-DD HH:MM, in UTC.
CREATE TABLE deliveries (
    delivery_id TEXT PRIMARY KEY NOT NULL,
    promised_at TEXT NOT NULL,
    delivered_at TEXT
);

INSERT INTO deliveries VALUES
    ('D101', '2026-10-19 12:00', '2026-10-19 11:50'),
    ('D102', '2026-10-19 12:00', '2026-10-19 12:20'),
    ('D103', '2026-10-19 12:00', '2026-10-19 11:40'),
    ('D104', '2026-10-19 12:00', NULL);

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
