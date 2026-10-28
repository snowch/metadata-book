# Metadata systems

Understand what your data means, where it came from, and how much you can trust the records describing it.

This book is for software and data engineers who can read a table and a simple SQL query. It follows a parcel-delivery company from a disputed percentage to the decisions involved in running a metadata system. Every result needed to follow the explanation is included on the page. There is nothing to install before reading.

<aside class="reader-action" aria-labelledby="before-you-start">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="before-you-start">Before you start</p>
<p><a href="metadata-map.md"><strong>Open the Metadata map</strong></a> for an overview of the book. The whole map shows how the records fit together. Select a record to highlight its connections, then choose <strong>Example record</strong> for its values or <strong>Fields &amp; types</strong> for its field definitions. Select its chapter badge to read the explanation.</p>
<p>Return using the header’s <strong>Metadata map</strong> button as you read; it highlights your current chapter. Click the button again to return to your reading.</p>
</div>
</aside>

## Contents

1. [What the data cannot tell you](chapters/01-why-metadata.md) — decide what a number should mean and record that decision.
2. [What a database already knows](chapters/02-reading-a-database.md) — inspect SQLite's records and check what a saved query actually counts.
3. [Where did this number come from?](chapters/03-following-lineage.md) — follow a report result to the run, code and inputs that produced it.
4. [Why is this report out of date?](chapters/04-outdated-reports.md) — explain a failed publication, check recovery and preserve the earlier evidence.
5. [Collecting metadata from several systems](chapters/05-collecting-metadata.md) — connect descriptions without confusing different tables, sources or times.
6. [When the records are unreliable](chapters/06-unreliable-records.md) — handle missing, repeated, late and conflicting observations.
7. [Using metadata to make decisions](chapters/07-using-metadata.md) — choose a suitable dataset and investigate the effects of a proposed change.
8. [Choosing and operating a metadata platform](chapters/08-choosing-a-platform.md) — test a platform against useful tasks and plan the work of keeping it reliable.
9. [Sharing metadata between systems](chapters/09-sharing-metadata.md) — follow an OpenLineage event from its producer to catalogue records and a query API.
10. [Managing definitions and dataset changes](chapters/10-managing-changes.md) — review changes, approve versions and preserve responsibility and history.
11. [Controlling access and enabling reuse](chapters/11-access-and-reuse.md) — connect permitted uses to controls, retention and research publication descriptions.

## How to read

Chapters 1–4 explain how to question a number and inspect the evidence behind it. They form a useful stopping point if your main task is reading reports or reviewing calculations. Chapters 5–8 cover collecting, using and operating metadata. Chapters 9–11 follow the records across system boundaries, organisational changes and access or reuse decisions.

People need different evidence from the same system. One person may hold several of these roles:

| Role | Question metadata should help answer |
|---|---|
| Analyst or report reader | Does this measure answer my question, and is its evidence current? |
| Producer or pipeline engineer | What did this execution read and write, and which consumers could a change affect? |
| Definition owner or steward | Who agreed this meaning, which version applies, and who must review a change? |
| Security, privacy or audit reviewer | Which uses are approved, where are restrictions enforced, and what evidence is retained? |
| Researcher or external consumer | Can I find, cite, access and reuse this version under its stated conditions? |

Worked examples carry the explanation. Each chapter’s **Core points** recap its main lessons. Records, query outputs and decisions appear beside the questions they answer, with highlighted fields and short explanations. No code execution is needed. Each chapter ends with a short, optional map activity and a collapsible answer. Chapters 1–3 also offer captioned videos with transcripts.

The company and its records are invented. The database examples and the incident simulation supporting Chapters 3–4 use the real SQLite engine. The additional debugging scenario, collection histories, decisions, pilot assessment and publication descriptions are illustrative. The OpenLineage event is checked against its schema; it is not captured from a running integration. Product-specific explanations link to the tools' documentation. To run the examples yourself, see [Reproducing the worked results](examples/README.md).
