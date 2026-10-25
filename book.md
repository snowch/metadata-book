# Metadata systems

Understand what your data means, where it came from, and how much you can trust the records describing it.

This book is for software and data engineers who can read a table and a simple SQL query. It follows a parcel-delivery company from a disputed percentage to the decisions involved in running a metadata system. Every result needed to follow the explanation is included on the page. There is nothing to install before reading.

## Contents

1. [What the data cannot tell you](chapters/01-why-metadata.md) — decide what a number should mean and record that decision.
2. [What a database already knows](chapters/02-reading-a-database.md) — inspect SQLite's records and check what a saved query actually counts.
3. [Following a number to its source](chapters/03-following-lineage.md) — trace an outdated report to the run and inputs that produced it.
4. [Collecting metadata from several systems](chapters/04-collecting-metadata.md) — connect descriptions without confusing different tables, sources or times.
5. [When the records are unreliable](chapters/05-unreliable-records.md) — handle missing, repeated, late and conflicting observations.
6. [Using metadata to make decisions](chapters/06-using-metadata.md) — choose a suitable dataset and investigate the effects of a proposed change.
7. [Choosing and operating a metadata platform](chapters/07-choosing-a-platform.md) — test a platform against useful tasks and plan the work of keeping it reliable.

## How to read

Chapters 1–3 explain how to question a number and inspect the evidence behind it. They form a useful stopping point if your main task is reading reports or reviewing calculations. Continue through Chapters 4–7 if you also collect, maintain or choose tools for metadata.

Worked examples carry the explanation. Highlighted principles mark the central idea; **Further detail** boxes are optional. You can skip them without losing the argument.

The company and its records are invented. The SQLite examples use the real database engine; the incident histories are illustrative, and the platform pilot is a suggested exercise. Product-specific explanations link to the tools' documentation. To run the database example yourself, see [Reproducing the worked results](examples/README.md).
