# Metadata systems

A technical book about understanding, collecting and using metadata. Eleven focused chapters follow a parcel-delivery example from metric definitions to collecting evidence, exchanging records, governing changes and enabling controlled reuse.

**[Read the book](https://snowch.github.io/metadata-book/)** · [Contents in Markdown](book.md)

## Chapters

1. [What the data cannot tell you](chapters/01-why-metadata.md)
2. [What a database already knows](chapters/02-reading-a-database.md)
3. [Where did this number come from?](chapters/03-following-lineage.md)
4. [Why is this report out of date?](chapters/04-outdated-reports.md)
5. [Collecting metadata from several systems](chapters/05-collecting-metadata.md)
6. [When the records are unreliable](chapters/06-unreliable-records.md)
7. [Using metadata to make decisions](chapters/07-using-metadata.md)
8. [Choosing and operating a metadata platform](chapters/08-choosing-a-platform.md)
9. [Sharing metadata between systems](chapters/09-sharing-metadata.md)
10. [Managing definitions and dataset changes](chapters/10-managing-changes.md)
11. [Controlling access and enabling reuse](chapters/11-access-and-reuse.md)

The reading path needs no installation or code execution. Worked results are included. The SQLite fixture and the incident simulation supporting Chapters 3–4 run with Python's standard library. The simulation records inputs, code versions, failed publication and recovery locally; it is not a captured production trace.

## Evaluate the approach

Read the chapters in order, then consider:

- Where did you have to reread a passage to understand it?
- Which explanations could be cut without losing understanding?
- Did the SQLite and lineage examples make the ideas useful beyond this scenario?
- Would running an example add understanding, or did the worked result do enough?

The chapters present definitions, database outputs, execution records, catalogue entries and decisions beside the questions they answer, using styled cards and comparisons in the main reading path. Runnable code and implementation notes remain supporting material. This approach makes the evidence concrete without requiring exercises or setup. Each chapter also ends with an optional map activity: two exploration steps, one question and a collapsed answer.

Chapters 1–4 form a short reading path about interpreting data. Chapters 5–8 cover collecting, using and operating metadata. Chapters 9–11 cover exchange and APIs, governance, access and FAIR reuse. The contents explain different readers’ roles; Chapter 9 diagrams the system that maintains and serves the records. Implementation notes and reproduction instructions remain in the supporting examples; there is no separate lab requirement or browser database runtime.

## Metadata map

The header’s Metadata map button opens a [visual index](metadata-map.md), highlighting the originating chapter. Clicking it again closes the map and returns to the reading page; direct visits return to their linked chapter or the contents. The map shows all 19 record types and 23 relationships in a stable layout. Selecting a record highlights its direct connections without moving or hiding the others. Zoom and scroll (or drag the background) to explore; Fit restores the overview. A collapsible **Connections as text** section provides a text alternative for the selected record. Three tabs—Map, Example record, and Fields & types—preserve the selected record on every screen size. The selected name stays above the tabs, and returning to the map preserves its zoom and position. Chapter badges link to the explanations in the book. A “Before you start” panel on the contents page introduces the map. Without JavaScript, the records remain readable.

The map uses local HTML, CSS and JavaScript with no third-party browser runtime or network requests. Its illustrative model lives in `assets/metadata-map.json`; computed examples are checked against SQLite. The whole-map geometry is precomputed in `assets/metadata-map-layout.json`. After changing record types or relationships, install Graphviz and run `python3 scripts/generate_map_layout.py`. Normal builds and `--check` use the saved layout without Graphviz. Only the map page loads its interactive code.

## Build and verify

Requires Python 3.11 or later.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/verify_examples.py
python3 scripts/verify_metadata_map.py
python3 scripts/generate_map_layout.py --check
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. The generated site uses static HTML and CSS, a locally hosted Newsreader typeface and relative links. The Pages workflow builds and publishes pushes to `main` using GitHub Actions.

To check the map interactions locally after building (optional development dependencies):

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/verify_map_browser.py
```

This checks chapter context, linked examples, keyboard tabs, URL state, mobile layouts and the no-JavaScript fallback. The Pages workflow runs the data and link checks without installing a browser.

## Sources and examples

Product-specific references appear beside the relevant explanations. The parcel company and delivery records are original, invented teaching examples. [examples/README.md](examples/README.md) explains the executable fixture, local incident simulation and their limits.

## Chapter videos

Chapters 1–11 include narrated page learning aids with optional English captions and transcripts. Final media is published in each chapter's directory under `assets/video/`. Source and rebuild instructions for [Chapter 1](video/chapter-01/README.md), [Chapter 2](video/chapter-02/README.md), [Chapter 3](video/chapter-03/README.md), [Chapter 4](video/chapter-04/README.md), [Chapter 5](video/chapter-05/README.md), [Chapter 6](video/chapter-06/README.md), [Chapter 7](video/chapter-07/README.md), [Chapter 8](video/chapter-08/README.md), [Chapter 9](video/chapter-09/README.md), [Chapter 10](video/chapter-10/README.md) and [Chapter 11](video/chapter-11/README.md) retain the narration, scene plans and rendering workflow. The players do not autoplay or preload the MP4. Working media and caches remain in ignored `out/`. The [video workflow](video/README.md) includes an unprompted pronunciation audit immediately after narration generation, before rendering.
