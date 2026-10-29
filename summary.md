# Putting it all together

**Metadata describes data’s structure, meaning, origin and use.** Across this book, the practical task has been to connect a question to the records that can answer it—and make clear what those records leave uncertain.

Use this page to revisit the eleven chapters or explain their lessons in your own words. Each chapter link returns to its examples, video and practice activity. The company and records are invented; the later policy decisions, platform assessment and research release are illustrative, not reports of a deployed system.

## Understand and explain a result

### 1. Agree what the number means

The same four parcels give **66.7% among completed deliveries** and **50.0% among all deliveries due**. The unfinished parcel changes the denominator. Record the population, cutoff, meaning and responsible team, then check that the calculation implements the rule. A correct calculation can answer the wrong question. [Revisit Chapter 1](chapters/01-why-metadata.md).

### 2. Inspect structure and calculation

Database metadata exposes columns, declared types, constraints and saved query definitions. It does not settle business meaning. In the SQLite example, the view’s filter removes unfinished deliveries; the column name cannot tell us whether a promise is original or revised. Distinguish what the database permits, what values mean and what the query actually counts. [Revisit Chapter 2](chapters/02-reading-a-database.md).

### 3. Trace the result to its evidence

Dependencies show a possible route through systems. Execution records connect a particular report refresh to an output, its producing run, retained input and code. **Lineage** describes origins, transformations and dependencies; **provenance** records creation and change history, including sources and methods. The terms overlap. Follow matching identifiers and inspect the retained evidence. Explaining a historical result does not establish that it is current. [Revisit Chapter 3](chapters/03-following-lineage.md).

### 4. Prove recovery reaches the reader

The report’s old **100%** remains explainable after a later publication fails. Recovery needs both a successful new publication and a refresh that reads it. A successful run can also calculate the wrong rule, so inspect its inputs and code. Keep earlier evidence to explain what readers saw. [Revisit Chapter 4](chapters/04-outdated-reports.md).

## Collect evidence and use it for decisions

### 5. Join identities without merging authority

A database scan supplies structure, a scheduler reports execution and a definition supplies intended meaning. Agree dataset identities across sources; matching table names alone are insufficient. Keep each claim’s source, observation or event time, and collection time. Collection does not establish creation time, accepted ownership or authority over every fact. [Revisit Chapter 5](chapters/05-collecting-metadata.md).

### 6. Preserve uncertainty when records disagree

Missing from a scan does not necessarily mean deleted: check scope, permissions and completion. Recognise repeated messages using source and stable event identity; a fresh observation of unchanged state is still a new observation. A late arrival can describe an earlier event. Preserve conflicting claims and show a disputed state until supporting evidence resolves it. [Revisit Chapter 6](chapters/06-unreliable-records.md).

### 7. Match evidence to the decision

Search terms and glossary synonyms help discovery; scope and definitions determine suitability. A data contract records commitments about structure, meaning, quality, delivery and changes. A quality result records what a particular check observed on a particular input. Neither passing checks nor popularity proves fitness for every purpose. Record the chosen rule, missing evidence, next action and owner; use dependencies as a starting point for change review, allowing for unrecorded consumers. [Revisit Chapter 7](chapters/07-using-metadata.md).

### 8. Test a small, maintainable arrangement

Use a bounded pilot with known questions and an independent reviewer who can open the evidence. Check coverage, export fidelity, collection failure and access paths. Budget ongoing maintenance, assign owners and agree freshness limits. The invented pilot keeps documents and SQLite within its scope and budget; it does not assess a catalogue product or establish wider coverage. Expand only with evidence that the arrangement works and reduces effort. [Revisit Chapter 8](chapters/08-choosing-a-platform.md).

## Share, change and reuse responsibly

### 9. Connect systems explicitly

An event format does not establish delivery, permissions or matching identities. Configure producer and receiver, retain namespaces and run UUID mappings, and check retries, gaps and when accepted records become queryable. OpenLineage’s event model, CloudEvents’ envelope and a catalogue’s query API serve different purposes. A completion event naming datasets still needs additional snapshot, code, output-version and refresh records to explain a particular result. [Revisit Chapter 9](chapters/09-sharing-metadata.md).

### 10. Review meaning and release evidence

An unchanged column name and type can conceal a change from original to revised promise, affecting both punctuality and denominator membership. Separate proposal, design approval and release; record consumer agreement, effective dates, validation and actual publication evidence. Dataset, contract, definition and output versions identify different things. A steward coordinates review; business owners decide definitions. Retain accepted ownership transfers and traceable restatements without erasing earlier reports. [Revisit Chapter 10](chapters/10-managing-changes.md).

### 11. Connect permitted use to controls and reuse conditions

A restricted label or approved purpose is not an enforced permission. Apply and test controls across database access, catalogue visibility, APIs and exports. Protect queries, samples and copies; retain artifacts by purpose and state what deletion prevents you from reproducing. FAIR means **Findable, Accessible, Interoperable and Reusable**; it neither requires public access nor grants permission or guarantees quality or compliance. The planned synthetic release is separate from operational data, with its identifier and license still proposed or pending. [Revisit Chapter 11](chapters/11-access-and-reuse.md).

## Connect the records before making a claim

For a report investigation, follow **report refresh → published output → producing run → retained input and code**, then compare the calculation with the agreed definition. This traces the result backwards; it is not the order in which the data was produced.

Along that trail, check the source and times of each claim, missing or conflicting observations, and whether you are permitted to inspect and use the evidence. For a proposed change, add consumer review and release records. For reuse, add purpose, version, license, access and retention conditions. The [Metadata map](metadata-map.md) lets you inspect these kinds of record and their connections; nearby examples are not automatically evidence of the same event.

The book’s percentages answer different questions about different evidence:

| Result | What it describes |
|---|---|
| 100% | The earlier published completed-delivery result read by the stale report. |
| 66.7% | Two on-time deliveries out of three completed in the four-parcel example. |
| 50.0% | Two on-time deliveries out of all four due—the operations meeting’s chosen rule. |

Refreshing the completed-delivery report can address its age; it does not change its denominator. The meeting’s illustrative decision still needs a verified all-due calculation and publication attached.

## Check what you can explain

Before opening the answers, explain these to a colleague or write a sentence for each. Try again later without rereading, then apply the questions to a report you know.

1. Why can a report be fresh and correctly calculated yet unsuitable for a meeting?
2. What is missing if you have a dependency diagram and a successful run status, but need to explain a displayed number?
3. Why does a dataset’s absence from today’s scan need investigation?
4. Why can an approved schema change still be unready for release?
5. Why does the planned public synthetic dataset not authorise sharing operational deliveries?

<details markdown="1">
<summary>Check your answers</summary>

1. Its definition may answer a different question. Completed deliveries exclude the unfinished parcel; the meeting needs all deliveries due. Freshness and arithmetic do not choose the right population.
2. You need the actual refresh-to-output-to-run links, retained input and code, and the definition used to judge the calculation. A dependency is a possible route; success does not prove the right values reached the reader.
3. The collector may lack permission, cover the wrong scope or stop early. Keep the last successful observation visible and mark current status unverified until deletion has supporting evidence.
4. Design approval does not supply consumer acceptance and migration evidence, validation or a rollout plan. Meaning can change despite compatible structure. After release, actual execution and refresh records establish what consumers received.
5. The records concern different datasets and purposes. The research example is wholly synthetic and still planned; its proposed license and pending identifier neither establish a completed release nor permission to export operational records.

</details>

For your own dataset, leave a decision someone can act on: **the question, applicable definition and version, supporting evidence, unresolved gaps, permitted use, next action and responsible person**.
