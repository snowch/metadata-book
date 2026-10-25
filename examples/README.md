# Reproducing the worked results

The book is readable without execution. To check its SQLite results, run this from the repository root:

```sh
python3 scripts/verify_examples.py
```

This uses Python's standard-library SQLite engine in memory. It creates no persistent database and requires no network access. The SQL fixture is in [deliveries.sql](deliveries.sql).

The four delivery records are invented. All timestamps share the format `YYYY-MM-DD HH:MM` and are UTC. At the 13:00 snapshot, two deliveries are on time, one is late and one is not recorded as completed. A null means no recorded completion in this fixture; this is a scenario assumption, not a universal interpretation of nulls.

The verifier checks the actual catalogue queries and view result printed in Chapter 2, both denominators from Chapter 1, and the empty-input behaviour. It also computes the earlier 12:05 result used in Chapter 3, by removing D102's later completion from a copy of the fixture. The job failures, publication history and report refresh in that chapter are illustrative evidence, not events emitted by this script or a live dbt/OpenLineage deployment.

The SQL example runs natively for verification. A browser WASM database is not included; that would be a separate optional reading feature, subject to measuring its usefulness and loading cost.
