SELECT r.run_id, r.code_version, r.input_snapshot_id
FROM report_refreshes AS f
JOIN outputs AS o ON o.output_version = f.output_version
JOIN runs AS r ON r.run_id = o.run_id
WHERE f.refresh_id = 'F1300';
