# Metadata systems

Understand what your data means, where it came from, and how much you can trust the records describing it.

This book is for software and data engineers who can read a table and a simple SQL query. It follows a parcel-delivery company from a disputed percentage to the decisions involved in running a metadata system. Every result needed to follow the explanation is included on the page. There is nothing to install before reading.

## Contents

1. [What the data cannot tell you](chapters/01-why-metadata.md) — decide what a number should mean and record that decision.
2. [What a database already knows](chapters/02-reading-a-database.md) — inspect SQLite's records and check what a saved query actually counts.
3. [Where did this number come from?](chapters/03-following-lineage.md) — follow a report result to the run, code and inputs that produced it.
4. [Why is this report out of date?](chapters/04-outdated-reports.md) — explain a failed publication, check recovery and preserve the earlier evidence.
5. [Collecting metadata from several systems](chapters/05-collecting-metadata.md) — connect descriptions without confusing different tables, sources or times.
6. [When the records are unreliable](chapters/06-unreliable-records.md) — handle missing, repeated, late and conflicting observations.
7. [Using metadata to make decisions](chapters/07-using-metadata.md) — choose a suitable dataset and investigate the effects of a proposed change.
8. [Choosing and operating a metadata platform](chapters/08-choosing-a-platform.md) — test a platform against useful tasks and plan the work of keeping it reliable.

## How to read

Chapters 1–4 explain how to question a number and inspect the evidence behind it. They form a useful stopping point if your main task is reading reports or reviewing calculations. Continue through Chapters 5–8 if you also collect, maintain or choose tools for metadata.

Worked examples carry the explanation. Each chapter’s **Core points** recap its main lessons; **Further detail** boxes are optional. You can skip them without losing the argument. Records, query outputs and decisions appear beside the questions they answer, with highlighted fields and short explanations. No code execution is needed.

The company and its records are invented. The database examples and the incident simulation supporting Chapters 3–4 use the real SQLite engine. The collection histories, decision records and pilot assessment are illustrative examples, not results from testing a live catalogue. Product-specific explanations link to the tools' documentation. To run the examples yourself, see [Reproducing the worked results](examples/README.md).
