# Chapter 9 scene plan

Audience: engineers and report investigators. Embedded aid. Source: chapters/09-sharing-metadata.md at eec9cf06927910c7eef2b73e437a03430d023cbb. Guidance: explainer f16d0350df20cb35681886cb5d197ce27f2d3a49.
Objective: Separate event format, delivery configuration and explicit identity mappings, and identify evidence missing from a completion event.
Takeaway: compatible format does not establish a connected, identifiable evidence chain.

| Scene | Source / visual | Interpretation guard |
|---|---|---|
| connection-question | Event document between producer and receiver with no established route; 4s hold | No running service or successful delivery implied |
| connection-answer | Format → configured route/permission → accepted → queryable distinction | Acceptance is under receiver contract; not exactly-once or immediate retrieval |
| identity-question | Same job name/R1205 in hypothetical two schedulers; 4s hold | A name collision is a teaching supposition, no production fact |
| identity-answer | Namespace + job; short label ↔ UUID; dataset pair ↔ local ID | Mappings explicit, run UUID reused only within same execution; no fabricated full UUID |
| limits | Completion claim vs missing snapshot/code/output-version/refresh; model/envelope/query distinction | Input/output dataset identities are not retained input/output versions; query API illustrative |
| practice | Map Run → Job; absence of namespace/exchange UUID identified | Map short IDs insufficient; example URLs not live services |
| end | Five-second practice card | Full event, configuration and credential handling remain on page |

Two four-second silent holds follow completed questions and captions. Stage evidence at unique sentence cues; preserve ASR originals, timing estimates and lexical expansions separately. Inspect actual encoded layers, phone view and browser. No human listening or learner outcome approval.
