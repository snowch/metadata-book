# Metadata systems

A technical book about understanding, collecting and using metadata. Seven chapters follow one parcel-delivery example from metric definitions to collecting evidence and choosing a platform.

**[Read the book](https://snowch.github.io/metadata-book/)** · [Contents in Markdown](book.md)

## Chapters

1. [What the data cannot tell you](chapters/01-why-metadata.md)
2. [What a database already knows](chapters/02-reading-a-database.md)
3. [Following a number to its source](chapters/03-following-lineage.md)
4. [Collecting metadata from several systems](chapters/04-collecting-metadata.md)
5. [When the records are unreliable](chapters/05-unreliable-records.md)
6. [Using metadata to make decisions](chapters/06-using-metadata.md)
7. [Choosing and operating a metadata platform](chapters/07-choosing-a-platform.md)

The reading path needs no installation or code execution. Worked results are included. The SQLite fixture and Chapter 3's incident simulation run with Python's standard library. The simulation records inputs, code versions, failed publication and recovery locally; it is not a captured production trace.

## Evaluate the approach

Read the chapters in order, then consider:

- Where did you have to reread a passage to understand it?
- Which explanations could be cut without losing understanding?
- Did the SQLite and lineage examples make the ideas useful beyond this scenario?
- Would running an example add understanding, or did the worked result do enough?

Chapter 3 is the benchmark for greater depth: a complete investigation, reproducible records, a recovery decision, retention tradeoffs and two questions with explained answers. The other chapters remain shorter while this approach is evaluated.

Chapters 1–3 form a short reading path about interpreting data. Chapters 4–7 cover collecting, using and operating metadata. Optional detail stays outside the core explanation; there is no separate lab requirement or browser runtime.

## Build and verify

Requires Python 3.11 or later.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/verify_examples.py
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. The generated site uses static HTML and CSS, a locally hosted Newsreader typeface and relative links. The Pages workflow builds and publishes pushes to `main` using GitHub Actions.

## Sources and examples

Product-specific references appear beside the relevant explanations. The parcel company and delivery records are original, invented teaching examples. [examples/README.md](examples/README.md) explains the executable fixture, local incident simulation and their limits.
