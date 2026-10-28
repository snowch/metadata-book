# 9. Sharing metadata between systems

The scheduler knows that `build_delivery_summary` finished. The catalogue needs that history, and a report investigator needs to retrieve it. Sharing metadata requires a common description, a delivery route and an agreement about identifiers. A compatible JSON document alone does not connect the systems.

## Where the records travel

<figure class="lineage-diagram metadata-architecture" aria-labelledby="exchange-caption">
<figcaption id="exchange-caption">From source evidence to consumers</figcaption>
<ol>
<li><span class="flow-role">Sources</span>Database, scheduler, definitions<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Collection</span>Collectors and events<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Catalogue</span>Identity and history<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Access</span>Search and API<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Consumers</span>Readers and policy engines</li>
</ol>
</figure>

Database collectors contribute structure; scheduler integrations contribute execution events; definition records contribute meaning and responsibility. The catalogue joins their claims using agreed identities and retains source and receipt times. Search pages and APIs expose that evidence. Policy metadata can describe who should have access, but a database or other enforcing engine must apply the rule. Saving a restriction in a catalogue does not itself block a query.

## Send a run event

[OpenLineage](https://openlineage.io/docs/spec/object-model/) defines common objects for jobs, runs and datasets, with events describing them. Here is an invented `COMPLETE` RunEvent for Chapter 3's execution. The [standalone JSON](../examples/exchange/complete-run-event.json) validates against the official [2-0-2 schema](https://openlineage.io/spec/2-0-2/OpenLineage.json), current when checked for this chapter.

```json
{
  "eventType": "COMPLETE",
  "eventTime": "2026-10-19T12:05:00Z",
  "run": {
    "runId": "019a9d87-d960-7000-8000-000000001205"
  },
  "job": {
    "namespace": "https://scheduler.example.invalid/prod",
    "name": "build_delivery_summary"
  },
  "inputs": [
    {
      "namespace": "postgresql://warehouse.example.invalid:5432",
      "name": "parcels.public.deliveries"
    }
  ],
  "outputs": [
    {
      "namespace": "postgresql://warehouse.example.invalid:5432",
      "name": "parcels.public.delivery_summary"
    }
  ],
  "producer": "https://example.invalid/integrations/scheduler/1.0",
  "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"
}
```

This adapts the incident to a hypothetical PostgreSQL deployment; the book's executable simulation still uses SQLite. The job's namespace separates this production scheduler from others. Each dataset's namespace identifies its system; its name identifies the database, schema and table here. The `producer` URI identifies the integration emitting the metadata, rather than the destination or the metric's owner. `schemaURL` identifies the event schema. None of these example addresses hosts a running service.

OpenLineage requires a UUID for `runId`. The book's short label `R1205` is not suitable. This example explicitly maps `R1205` to `019a9d87-d960-7000-8000-000000001205`; a real integration generates and persists a UUID for each execution. It reuses that UUID throughout the [run cycle](https://openlineage.io/docs/spec/run-cycle/), including `START` and the terminal event. This extract shows only completion. A new execution needs a new identity.

## Configure the connection

Enable an OpenLineage integration in the scheduler or instrument the job with a client. The integration must observe the execution, identify its datasets and emit events; setting a destination does not discover those facts automatically.

For example, the Python client's documented [HTTP configuration](https://openlineage.io/docs/client/python/configuration) can use:

```sh
OPENLINEAGE__TRANSPORT__TYPE=http
OPENLINEAGE__TRANSPORT__URL=https://catalogue.example.invalid
OPENLINEAGE__TRANSPORT__ENDPOINT=api/v1/lineage
OPENLINEAGE__TRANSPORT__AUTH__TYPE=api_key
```

The deployment's secret manager supplies `OPENLINEAGE__TRANSPORT__AUTH__APIKEY`; no credential belongs in the event or repository. This client sends JSON by HTTP POST and uses the configured key as a bearer token. The receiving service must support that endpoint and authentication scheme. Its permissions should allow the producer to submit the intended records. Other receivers may require different transports or authentication.

Confirm schema support, naming conventions, supported facets, errors and retry behaviour on both sides. A successful HTTP acknowledgement establishes acceptance under that service's contract; check when the record becomes queryable. Retries can duplicate deliveries, and failures can leave gaps. Agree how to identify repeated deliveries separately from distinct events for the same run, and retain occurrence and receipt times as in Chapter 6. Neither the JSON schema nor HTTP supplies an exactly-once guarantee.

## Interpret what arrived

The receiving adapter maps the output namespace/name pair above to `prod/parcels/delivery_summary`, using an explicit local naming rule. It also retains the UUID-to-`R1205` correspondence. These mappings are catalogue configuration, not identifiers that OpenLineage infers from the short table name.

<figure class="metadata-record">
<figcaption><span class="record-kind">Received run claim</span><span class="record-source">Illustrative catalogue record</span></figcaption>
<dl>
<div class="record-focus"><dt>Dataset</dt><dd><strong><code>prod/parcels/delivery_summary</code></strong></dd></div>
<div><dt>Reported outcome</dt><dd><code>R1205</code> completed at 12:05 UTC.</dd></div>
<div><dt>Received</dt><dd>2026-10-19 12:06 UTC</dd></div>
<div><dt>Source</dt><dd>Scheduler integration; original run UUID retained.</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this tells us</strong> The producer reported this job's completion and its input and output dataset identities.</p>
<p class="evidence-limit"><strong>What it does not tell us</strong> This event does not preserve input snapshot S1205, code completed-v1, output version summary-R1205 or the report refresh reference. It does not independently verify the written values. Chapter 3's investigation still needs those additional records.</p>

## Retrieve the assembled evidence

A catalogue can offer its own query API. This vendor-neutral request and response are **illustrative, not an OpenLineage standard**; the response fields belong to this example. An authorised reader supplies credentials separately; the server checks read permissions, independently of the producer's submission permissions.

```http
GET /api/datasets/prod%2Fparcels%2Fdelivery_summary/runs?limit=1 HTTP/1.1
Host: catalogue.example.invalid
Accept: application/json
```

```json
{
  "datasetId": "prod/parcels/delivery_summary",
  "runs": [{
    "runId": "019a9d87-d960-7000-8000-000000001205",
    "bookLabel": "R1205",
    "reportedState": "COMPLETE",
    "eventTime": "2026-10-19T12:05:00Z",
    "receivedAt": "2026-10-19T12:06:00Z"
  }]
}
```

OpenLineage supplies the lineage objects and event vocabulary. [CloudEvents](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#required-attributes) supplies a general event envelope, including source and event ID; a wrapping agreement could carry an OpenLineage payload, but these are distinct specifications. A catalogue API supplies retrieval operations, authentication, filtering and pagination. Supporting one does not automatically supply the others or make two catalogues interchangeable.

## Core points

- **Agree identities and mappings.** Dataset pairs and run UUIDs must survive the exchange.
- **Configure a producer and a receiver.** Format compatibility does not establish transport, permission or delivery guarantees.
- **Read events as sourced claims.** Retain additional evidence needed to explain a particular result.
- **Separate event models, envelopes and query APIs.** Each solves a different part of sharing metadata.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore this chapter in the map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=9&amp;record=run"><strong>Open the Metadata map</strong></a>, then choose <strong>Example record</strong>.</p>
<ol>
<li>Find <code>run_id</code> and <code>job_name</code>. Follow the job reference and check that its name matches.</li>
<li>Look at the fields that identify the run and job. Does this example include a job namespace or an OpenLineage run UUID?</li>
</ol>
<p><strong>Think about it:</strong> Would sending these short identifiers alone reliably identify the execution in another system?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>No. Names such as <code>build_delivery_summary</code> can occur in different schedulers. The receiver needs the namespaced job identity and an explicit mapping from <code>R1205</code> to the exchange run UUID. Those mappings are additional metadata; this map example does not contain them. A shared format also does not establish transport or access permission.</p>
</details>
<p>Return here using the header’s <strong>Metadata map</strong> button.</p>
</div>
</aside>
