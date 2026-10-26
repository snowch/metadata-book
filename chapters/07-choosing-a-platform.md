# 7. Choosing and operating a metadata platform

A metadata platform should help a team complete a task it currently struggles with. Start with that task and a small body of evidence.

## Set a small pilot

Give the reporting engineer and a Delivery Operations reviewer one week to answer two questions: which measure belongs in the operations meeting, and why did Delivery performance show 100% at 13:00 on 19 October?

Use the definitions, `deliveries` and `on_time_completed` structure, the `build_delivery_summary` dependency path, and the incident's run, publication and refresh records. Include references to the retained inputs. These are a deliberately small collection with known answers: the meeting requires the all-due rule, while the incident report read `summary-R1205` after a later run failed.

Try the investigation with a repository of reviewed documents and a few SQLite tables, then assess whether DataHub or OpenMetadata would solve a problem encountered during that investigation. No installation is needed to follow this chapter. The [DataHub documentation](https://docs.datahub.com/docs/) and [OpenMetadata documentation](https://docs.open-metadata.org/) describe current capabilities; verify support for the exact source and version you need.

## Test what the reader can establish

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Acceptance checks for the parcel pilot</figcaption>

| Task | Pass condition |
|---|---|
| Choose the meeting measure | The reviewer finds both denominator definitions, selects all-due and explains the expected 50.0%. |
| Explain the incident | The reviewer follows the refresh to `summary-R1205`, its successful run and retained inputs, and identifies the later run that failed before publishing. |
| Recognise incomplete collection | A deliberately failed metadata collection leaves the last successful observation time and a visible failure; the reviewer recognises the records may be outdated. |
| Respect access boundaries | A permitted reviewer can follow the necessary evidence; a restricted account cannot retrieve protected descriptions through search, links or an API. |

</figure>

Run these checks with someone who did not assemble the records. Ask them to show the evidence behind each answer. A link to saved input data is useful only if the reviewer can open it.

For collection, name the exact systems covered: database structure, scheduled jobs and report refreshes may require different collectors. A collector is software that reads metadata from a source. Check which records each one actually supplies and which this pilot entered by hand. Preserve the source identifier, observation time and version references when importing or exporting records; otherwise a platform move can break the incident's evidence chain.

## Budget for the work after setup

A repository makes definitions easy to review alongside code. SQLite can join the incident records by identifier. Someone must still collect changes, maintain links, control access and help readers find them. Evaluate a catalogue when those jobs slow the team down; use the pilot to measure whether it helps.

Assign the reporting engineer responsibility for collection failures. Delivery Operations owns the all-due definition; Service Analytics owns the completed-delivery definition. Agree how soon source changes must appear. Review the age of the last successful collection, investigate failures and renew access credentials when needed. When upgrading a collector, rerun the pilot checks: changed identifiers, missing fields or altered permissions can silently break an investigation. Retain enough history to explain past reports after current definitions change.

## Decide what happens next

Use the pilot results to decide what happens next:

- **Keep the current approach** if the repository and SQLite pass all four checks at manageable effort.
- **Extend the catalogue trial** to one additional report if it passes and measurably reduces collection or investigation work.
- **Fix the gaps first** if neither passes. Stop expansion and address the missing evidence or access path.

Finish the pilot with its check results, collection coverage, named owners and a recorded choice. The next operations meeting should receive a verified all-due calculation with its definition and output reference attached. That is a concrete result against which the platform's continuing cost can be judged.

## Core points

- **Start with a small task and known answers.** Test whether a reader can find a suitable measure and explain a reported result.
- **Check evidence, collection coverage and access.** Verify what each collector supplies and what each reader can retrieve.
- **Plan for continuing work.** Assign responsibility for definitions and collection failures, monitor freshness, and maintain access and history.
- **Choose the smallest arrangement that passes the checks.** Expand only when it works and reduces the team's effort; fix evidence or access gaps first.
