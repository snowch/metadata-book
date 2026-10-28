# A lineage exchange record

[Chapter 9](../../chapters/09-sharing-metadata.md) prints `complete-run-event.json` verbatim. It is an invented OpenLineage completion event for Chapter 3's R1205, not a message captured from a service. No requests are sent by this example. The source and destination systems remain illustrative, and no credentials are included.

The event was checked against the official [OpenLineage 2-0-2 schema](https://openlineage.io/spec/2-0-2/OpenLineage.json), also identified by the upstream repository's current `spec/OpenLineage.json` when checked on 28 October 2026. Validation includes UUID, URI and date-time format checks. It establishes structural conformance, not truthful execution evidence or receiver compatibility.

To repeat the check from the repository root in an environment with Python's optional `jsonschema` package available, download the schema with TLS verification enabled:

```sh
curl -fsSL https://openlineage.io/spec/2-0-2/OpenLineage.json -o /tmp/openlineage-schema.json
python3 - <<'PY'
import json
from jsonschema import validators, FormatChecker

with open('/tmp/openlineage-schema.json') as source:
    schema = json.load(source)
with open('examples/exchange/complete-run-event.json') as source:
    event = json.load(source)
validator_class = validators.validator_for(schema)
validator_class.check_schema(schema)
validator_class(schema, format_checker=FormatChecker()).validate(event)
print('OpenLineage event is valid')
PY
```

This requires no database, scheduler, catalogue or OpenLineage service. It does not emit `START` or test delivery, authentication, retention or queries. Chapter 9's catalogue query API is a separate invented interface, not part of the OpenLineage schema.
