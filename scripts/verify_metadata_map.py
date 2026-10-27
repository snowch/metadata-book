"""Validate map references and its computed examples against the book's SQLite data."""

import importlib.util
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def verify():
    data = json.loads((ROOT / 'assets/metadata-map.json').read_text())
    records = {record['id']: record for record in data['records']}
    assert len(records) == len(data['records']) == 17, 'Missing or duplicate record type'
    groups = {group['id'] for group in data['groups']}
    chapters = {chapter['number']: chapter for chapter in data['chapters']}
    assert set(chapters) == set(range(1, 9)), 'Map must cover all eight chapters'
    covered = set()
    for record in records.values():
        assert re.fullmatch(r'[a-z][a-z-]*', record['id'])
        assert record['group'] in groups
        assert record['fields'] and record['description'] and record['interpretation']
        assert record['primaryChapter'] in {link['number'] for link in record['chapters']}
        for link in record['chapters']:
            assert link['number'] in chapters
            assert link['href'].startswith(chapters[link['number']]['href'] + '#'), link
            covered.add(link['number'])
        assert len({field['name'] for field in record['fields']}) == len(record['fields'])
        for field in record['fields']:
            assert isinstance(field['value'], str), (record['id'], field)
            assert field['type'] and field['description']
            if 'target' in field:
                assert field['target'] in records, field
        for relation in record['related']:
            assert relation['target'] in records and relation['label']
    assert covered == set(chapters)
    for relation in data['relationships']:
        assert relation['from'] in records and relation['to'] in records
        assert relation['from'] != relation['to'] and relation['label']
    assert {'from': 'published-output', 'to': 'run', 'label': 'produced by'} in data['relationships']

    def fields(record_id):
        return {field['name']: field['value'] for field in records[record_id]['fields']}

    assert fields('data-contract')['Identifier rule'] == fields('quality-rule')['Rule']
    assert fields('quality-check')['Identifier rule'] == fields('quality-rule')['Rule']
    assert fields('quality-rule')['Contract'] == fields('data-contract')['Contract']
    assert fields('quality-rule')['Dataset'] == fields('data-contract')['Dataset'] == fields('dataset')['name']
    for edge in [('data-contract', 'quality-rule', 'includes'), ('quality-check', 'quality-rule', 'evaluates')]:
        assert dict(zip(('from', 'to', 'label'), edge)) in data['relationships']

    path = ROOT / 'examples/lineage/simulate.py'
    spec = importlib.util.spec_from_file_location('map_simulation', path)
    simulation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simulation)
    db = simulation.build_incident()
    try:
        for record_id, table, key in [
            ('run', 'runs', 'run_id'),
            ('input-snapshot', 'snapshots', 'snapshot_id'),
            ('published-output', 'outputs', 'output_version'),
            ('report-refresh', 'report_refreshes', 'refresh_id'),
        ]:
            printed = fields(record_id)
            cursor = db.execute(f'SELECT * FROM {table} WHERE {key} = ?', (printed[key],))
            row = cursor.fetchone()
            assert row is not None, record_id
            actual = dict(zip((column[0] for column in cursor.description), row))
            for name, value in printed.items():
                assert value == str(actual[name]), (record_id, name, value, actual[name])
        assert fields('report-refresh')['output_version'] == fields('published-output')['output_version']
        assert fields('published-output')['run_id'] == fields('run')['run_id']
        assert fields('run')['input_snapshot_id'] == fields('input-snapshot')['snapshot_id']
        assert fields('run')['code_version'] == fields('code-version')['code_version']
        assert fields('run')['job_name'] == fields('job')['job_name']
        retained = db.execute('SELECT sql_text FROM code_versions WHERE code_version = ?',
                              (fields('code-version')['code_version'],)).fetchone()[0]
        assert records['code-version']['code'].strip() == retained.strip()
        rows = db.execute('''SELECT delivery_id, promised_at, delivered_at FROM snapshot_rows
                             WHERE snapshot_id = ? ORDER BY delivery_id''',
                          (fields('input-snapshot')['snapshot_id'],)).fetchall()
        printed_rows = records['input-snapshot']['rows']
        assert printed_rows['columns'] == ['delivery_id', 'promised_at', 'delivered_at']
        assert printed_rows['values'] == [[str(v) if v is not None else 'NULL' for v in row] for row in rows]
        column = db.execute("SELECT name,type,\"notnull\",pk FROM pragma_table_xinfo('deliveries') WHERE name='delivered_at'").fetchone()
        assert [fields('column')[name] for name in ('name', 'type', 'notnull', 'pk')] == list(map(str, column))
        for record_id in ('dataset', 'saved-query'):
            printed = fields(record_id)
            assert db.execute('SELECT type FROM sqlite_schema WHERE name=?', (printed['name'],)).fetchone() == (printed['type'],)
        db.execute('DROP VIEW on_time_completed')
        db.executescript(records['saved-query']['code'])
        assert db.execute('SELECT * FROM on_time_completed').fetchone() == (3, 2, 66.7)
    finally:
        db.close()
    print('Verified metadata map: 17 record types, chapter references, directed relationships and SQLite examples.')


if __name__ == '__main__':
    verify()
