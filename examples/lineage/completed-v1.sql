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
