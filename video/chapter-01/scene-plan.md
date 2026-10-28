# Chapter 1 video content contract and scene plan

Source: [What the data cannot tell you](../../chapters/01-why-metadata.md), metadata-book commit `46e8224334d69d9ef9eee103f0b4def368a9f807`.
Workflow: [authored video workflow](https://github.com/snowch/explainer-video-generator/blob/ccr-970408dc-z6c1vo/docs/agent-video-workflow.md).

Audience: engineers and report readers; no SQL knowledge needed. Afterwards viewers should distinguish the two denominator choices, record a metric definition, and check its calculation. Standalone video, approximately 2.5–4 minutes; actual duration is measured from speech. Exact narration is in `narration.json`, not a separately paraphrased script. This is an authored adaptation, not a user-supplied verbatim narration.

One calm British narrator; no dramatic hook, music or unrelated imagery. Use the book's cream (#f7f4ed), ink (#292d29), rust (#96432e) and muted green palette. Coded parcel drawings explain inclusion; depot and customer drawings explain ambiguous field meaning. No decorative artwork. Source assumptions are visible and spoken. Complete definition remains visible during its explanation. Source credit and book URL close the video; no unverified copyright attribution.

| Scene kind | Chapter source | Exact on-screen ideas and coded visual | Reveal and inference to guard against |
|---|---|---|---|
| opening | What a number means | Four promised by noon; two on time, one late, one unfinished; invented example; complete records at 13:00 | Parcel statuses appear at the second sentence; do not generalise the meaning of missing timestamps. |
| completed | What a number means | Completed deliveries; 2 of 3; 66.7%; fourth parcel outside inclusion bracket | Bracket three at “Three parcels”; reveal result at “Two out of three”. Keep fourth parcel visible. |
| due | What a number means | All deliveries due; 2 of 4; 50.0% | Bracket all four at “All four parcels”; same two on-time parcels in numerator. |
| compare | What a number means | Both questions with their own denominator and result | Both valid for stated questions; no universal right/wrong colours. |
| metadata | Opening definition | Full definition: structure, meaning, origin and use; column/type, metric definition, producing job | Examples of metadata, not an exhaustive schema. |
| definition | Record the decision | Complete record: measure, on-time rule, all-due denominator, 13:00 UTC reporting date, Delivery Operations, deliveries table | Full definition stays on screen; highlight denominator as spoken. Do not confuse noon promise with measurement time. |
| owner | Record the decision | Delivery Operations: all due → 50.0%; another team: completed → 66.7% | Ownership explains intended meaning, not calculation correctness. |
| field | Record the decision | delivered_at branching to depot arrival? or customer arrival? | Question marks and “possible meanings” prevent either being asserted as actual source meaning. |
| mismatch | Check the calculation against the definition | Required denominator 4; query excludes unfinished, denominator 3; required 50.0%, displayed 66.7% | Highlight mismatch only for Delivery Operations' rule. |
| verify | Check the calculation against the definition | Filter → denominator → four-parcel example; rule and calculation both reviewed after change | Concrete checks, not an unsupported “verified” badge. |
| recap | Core points | What counts? When measured? Who explains it? Check calculation against rule | Definition and implementation receive equal emphasis. |
| end | Attribution | Chapter title, book link, adapted-from credit; synthetic narration disclosure | Five-second silent hold; no new claim. |

Provider word boundaries, not word-count estimates, determine reveal and caption timings. Independent clips and frozen audio make revisions possible. Source fidelity and scene meaning are reviewed manually; there is no automated faithfulness gate. Speech recognition is an automated audit, not a listening review.
