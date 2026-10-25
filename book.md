# Metadata systems

Understand what your data means, where it came from, and how much you can trust the records describing it.

This book is for software and data engineers who can read a table and a simple SQL query. It explains metadata systems through a small parcel-delivery example, worked investigations and real tools. Every result needed to follow the argument is included on the page. There is nothing to install before reading.

## Read the sample

These three complete chapters are the initial editorial sample. The company and its records are invented; the SQLite queries use the real database engine. The tool documentation linked in the chapters supports the product-specific explanations.

1. [What the data cannot tell you](chapters/01-why-metadata.md) — why two plausible calculations can disagree, and what a useful definition records.
2. [What a database already knows](chapters/02-reading-a-database.md) — inspect SQLite's own metadata and connect a view's definition to the result it produces.
3. [Following a number to its source](chapters/03-following-lineage.md) — investigate an outdated report and distinguish dependencies from evidence of an execution.

## The rest of the book

The remaining topics are an outline, not finished chapters. Their boundaries will change if the sample reveals a better pace.

| Working chapter | Question it answers |
|---|---|
| 4. Collecting metadata from several systems | How do identifiers, collection methods and differing observations fit together? |
| 5. When the records are unreliable | How should a system handle missing, duplicate, late and conflicting information? |
| 6. Using metadata to make decisions | What evidence supports discovery, quality assessment and change-impact analysis? |
| 7. Choosing and operating a metadata platform | What should we evaluate in a platform, and what work remains after installing it? |

The intended outcome is to be able to inspect a metadata source, distinguish its claims from its limits, follow a result through a system, and evaluate whether a platform records what a team needs. Optional exercises may accompany the book later; the core explanation will remain complete without them.
