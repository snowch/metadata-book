# 3. Following a number to its source

A report shows **100% of completed deliveries arrived on time**. A calculation using the current delivery records gives **66.7%**. Both use the same definition. Why do they disagree?

To answer, we need to follow the number back to the data and calculation that produced it.

## Lineage and provenance

<div class="definition-box" markdown="1">

**Lineage**

Records where data comes from, how it is transformed, and which datasets or reports depend on it.

</div>

<div class="definition-box" id="provenance" markdown="1">

**Provenance**

Records the history of a particular dataset or result: who or what created or changed it, when, and using which sources and methods.

</div>

Lineage emphasises **data flow**; provenance emphasises **creation and change history**. Both can describe transformations and the people or systems involved, so the distinction is not simply “how” versus “who.” The terms overlap in practice; lineage tools can also capture provenance.

## Follow the report's number

Another department, Service Analytics, measures the percentage of **completed deliveries that arrived on time**. It excludes parcels still awaiting delivery.

A scheduled job calculates this percentage from the delivery records and saves the result. The Delivery performance report reads that saved result whenever someone refreshes it. Refreshing the report does not rerun the calculation.

<figure class="lineage-diagram" aria-labelledby="lineage-caption">
<figcaption id="lineage-caption">How the number reaches the report</figcaption>
<ol>
<li><span class="flow-role">Source</span>Delivery records<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Calculation</span>Scheduled job<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Stored output</span>Saved percentage<span class="flow-arrow" aria-hidden="true">→</span></li>
<li><span class="flow-role">Report</span>Delivery performance</li>
</ol>
</figure>

This route tells us which job to investigate. It does not tell us which run of that job produced the number a reader saw.

Start with the report's refresh record: **which saved result did it read?** Then follow that result to the run that produced it. Looking only at the latest successful run could lead us to a result the report never read.

## Why 100% stayed on screen

In this invented incident, all four parcels were promised by noon. The delivery records are complete at each observation. All times below are UTC on 19 October 2026.

<figure class="worked-example incident-timeline" markdown="1">
<figcaption>Worked example · A fresh page, an old result</figcaption>

| Time | What happened |
|---|---|
| 12:05 | Two parcels had arrived, both on time. The job saved **2 out of 2: 100%**. |
| 12:20 | A third parcel arrived late. The current records now gave **2 out of 3: 66.7%**. The fourth parcel was still undelivered. |
| 12:30 | The next job run failed before saving a new result. The earlier 100% remained available. |
| 13:00 | The report refreshed and read the result saved at 12:05: **100%**. |

</figure>

The earlier calculation was correct for its inputs. The report was showing an older result, not calculating the current percentage incorrectly.

The failed run alone would not prove this. The report's refresh record connects the displayed 100% to the earlier saved result. Together, the records explain both how the number was calculated and why it remained on screen.

After fixing the failure, the team must check that a new run uses the updated delivery records, saves its result, and that the report actually reads it. A successful job alone does not establish what readers now see.

## Keep the evidence behind the result

To check the earlier 100%, we need more than today's delivery table:

- **The inputs that run read.** Today's records include a late delivery that was absent at 12:05.
- **The processing code it executed.** Today's query might use a different definition. A version label helps only if the corresponding code is still available.
- **The records connecting run, result and report.** These establish which calculation supplied the displayed number.

Running the original calculation against the retained 12:05 inputs reproduces 100%. Running it against the current inputs gives 66.7%. Different inputs explain the difference; we do not need to guess.

Keeping evidence has a cost. Agree how far back the team needs to investigate reports, then retain the necessary data, code and records for that period. Existing stored versions may avoid making extra copies, provided they remain available.

If the original inputs are deleted, a run record may still identify the source, but it cannot supply the missing rows. We can trace the result's recorded history without being able to reproduce its calculation.

## Core points

- **Lineage shows the route** from source data through processing to a report.
- **A particular result needs particular evidence:** the run, inputs and code that produced it.
- **Refreshing a report does not guarantee fresh data.** It may still read an older saved result.
- **Reproducing a calculation requires retained inputs and code**, not just references to them.

## Check your understanding

The processing job succeeds at 13:10. Is that enough to say the report now shows 66.7%?

<details class="further-detail" markdown="1">
<summary>Show answer</summary>

No. Check that the job used the updated inputs and saved the new result, then check that the report read that result. It could still be displaying the earlier 100%.

</details>

*Worked example: [The metadata behind an outdated report](../examples/lineage/walkthrough.md) shows the records that explain the displayed number, with each field and connection explained. No code execution is needed.*
