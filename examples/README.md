# Reproducing the worked results

The book is readable without execution. To check its SQLite results, run this from the repository root:

```sh
python3 scripts/verify_examples.py
```

This uses Python's standard-library SQLite engine in memory. It creates no persistent database and requires no network access. The SQL fixture is in [deliveries.sql](deliveries.sql).

The four delivery records are invented. All timestamps share the format `YYYY-MM-DD HH:MM` and are UTC. At the 13:00 snapshot, two deliveries are on time, one is late and one is not recorded as completed. A null means no recorded completion in this fixture; this is a scenario assumption, not a universal interpretation of nulls.

The verifier checks the catalogue queries and view result printed in Chapter 2, both denominators from Chapter 1, and the empty-input behaviour.

## Investigate the report in Chapters 3–4

[Chapter 3](../chapters/03-following-lineage.md) traces the original result, and [Chapter 4](../chapters/04-outdated-reports.md) explains the later publication failure and recovery. Both show the metadata records inline; no execution is required to read them. The supporting [lineage simulation](lineage/README.md) uses real SQLite tables for saved inputs, code versions, runs, published outputs and report refreshes. Run it with:

```sh
python3 examples/lineage/simulate.py
```

It computes the earlier 100% result, injects a publication failure, and then recovers to 66.7%. The earlier output and report refresh remain available after recovery. The same verifier checks those records, rollback after failure, replay using retained code and inputs, and rejection of missing evidence.

The incident's times and fault are scripted. The program demonstrates the evidence and publication behaviour locally; it does not connect to a live scheduler, reporting tool, dbt or OpenLineage service. It does not send alerts or enforce the simulation reference's suggested retention policy.

Chapters 5–7 use illustrative collection records and decisions, rather than records captured from a running catalogue. Chapter 8 shows an illustrative pilot assessment and decision. These are invented teaching records, not reported results from testing DataHub or OpenMetadata.

The SQL example runs natively for verification. A browser WASM database is not included; that would be a separate optional reading feature, subject to measuring its usefulness and loading cost.

## Sharing and governance examples

[Chapter 9’s OpenLineage event](exchange/README.md) is checked against the official JSON schema. It is an invented exchange record, not a captured message or live integration. The supplementary successful-but-wrong calculation in Chapter 4 and the change, access and research-release records in Chapters 10–11 are explicitly illustrative; they do not modify the simulation or publish data.
