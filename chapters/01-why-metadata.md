# 1. What the data cannot tell you

A dashboard shows a number. To use it, we need to know what it measures, where it came from, and how it was calculated. The values alone rarely supply those answers.

**Metadata is information that describes data:** its structure, meaning, origin and use. Column names and types are metadata. So are a metric's definition and a record of the job that produced it. These descriptions may live inside a database, alongside a report, or in a separate catalogue.

<figure class="chapter-video" aria-labelledby="chapter-video-title">
<figcaption id="chapter-video-title"><span>Watch the chapter</span><span class="chapter-video-duration">3 min 8 sec</span></figcaption>
<video controls playsinline preload="none" width="1280" height="720" poster="../assets/video/chapter-01/poster.jpg" aria-label="What the data cannot tell you: narrated Chapter 1 explainer" aria-describedby="chapter-video-note">
<source src="../assets/video/chapter-01/chapter-01.mp4" type="video/mp4">
<track kind="captions" src="../assets/video/chapter-01/captions.vtt" srclang="en" label="English">
Your browser cannot play this video. <a href="../assets/video/chapter-01/chapter-01.mp4">Download the video</a> or <a href="../assets/video/chapter-01/transcript.txt">read the transcript</a>.
</video>
<p class="chapter-video-note" id="chapter-video-note">The delivery example is invented and assumes complete records at the measurement time. Narration uses a synthetic voice.</p>
<p class="chapter-video-links"><a href="../assets/video/chapter-01/transcript.txt">Read the transcript</a><a href="../assets/video/chapter-01/chapter-01.mp4" download>Download video <span>(5 MB)</span></a></p>
</figure>

## What a number means

Even a familiar label such as “on-time delivery” leaves room for different calculations.

<figure class="worked-example" markdown="1">
<figcaption>Worked example · Two ways to count deliveries</figcaption>

A parcel company promised four deliveries by noon. At 13:00, two have arrived on time, one arrived late, and one has not arrived. This is an invented example; assume the delivery records are complete at that moment.

| Question | Calculation | Result |
|---|---|---:|
| Of the **completed deliveries**, how many were on time? | 2 out of **3** | 66.7% |
| Of **all deliveries due**, how many arrived on time? | 2 out of **4** | 50.0% |

Both calculations are valid for their stated questions. The first measures punctuality among completed deliveries. The second also counts the parcel still waiting to arrive. A dashboard labelled only “on-time delivery” leaves its readers to guess which question it answers.

</figure>

The disagreement comes from the denominator: the total number of deliveries included—three completed deliveries or all four deliveries due. Choosing that group is a business decision. A correct calculation can still answer the wrong question for the person reading the report.

## Record the decision

Suppose Delivery Operations uses the second definition: of all deliveries promised by noon, what proportion arrived on time? A useful definition would record:

<figure class="metadata-record">
<figcaption><span class="record-kind">Metric definition</span><span class="record-source">Decision by Delivery Operations</span></figcaption>
<dl>
<div><dt>Measure</dt><dd>Percentage of deliveries due that arrived on time</dd></div>
<div><dt>Counts as on time</dt><dd>Delivered at or before the promised time</dd></div>
<div class="record-focus"><dt>Denominator</dt><dd><strong>All deliveries due by noon, including those not yet delivered</strong></dd></div>
<div><dt>Measured at</dt><dd>13:00 UTC on the reporting date</dd></div>
<div><dt>Responsible team</dt><dd>Delivery Operations</dd></div>
<div><dt>Source</dt><dd>The <code>deliveries</code> table</dd></div>
</dl>
</figure>

<p class="evidence-reading"><strong>What this tells us</strong> All four parcels belong in the denominator, including the unfinished delivery. Two arrived on time, so the defined measure gives 50.0%.</p>

Another team could legitimately use the completed-delivery measure, provided its definition makes that choice clear.

The definition should name the team that can explain what the metric means—for example, Delivery Operations.

Column names also need explanation. Does `delivered_at` record when a parcel reached a depot or when it reached the customer? Both are plausible meanings; the name alone cannot tell us which one applies.

A recorded definition helps readers understand what a number measures. It also reveals when similarly named metrics count different things and should not be compared directly.

*Later in the book, [Chapter 8](08-choosing-a-platform.md) compares ways to store and maintain these definitions, from reviewed documents to a metadata catalogue.*

## Check the calculation against the definition

Recording a rule does not ensure that a query follows it. If the dashboard removes unfinished deliveries before counting, it will show 66.7% even though the recorded definition requires 50.0%.

The definition makes this disagreement testable. A reviewer can inspect the query's filters and denominator, then compare its output with the four-parcel example. If the intended rule changes, both the definition and the calculation need review.

A database already records some of the information that helps with this check: its table structure and saved query definitions. Those records are the starting point for the database example in Chapter 2.

## Core points

- **A metric must say what counts.** Completed deliveries and all deliveries due answer different questions, even when both are labelled “on-time delivery.”
- **Record the definition and responsible team.** Readers need to know what is included, when it is measured and whom to ask about its meaning.
- **A definition is something to check against.** Inspect the calculation to verify that its filters and denominator follow the recorded rule.

<aside class="reader-action" aria-labelledby="explore-metadata-map">
<svg class="reader-action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2V5Z"/><path d="M9 3v16M15 5v16"/></svg>
<div>
<p class="reader-action-title" id="explore-metadata-map">Explore the metadata map · 2 minutes</p>
<p><a href="../metadata-map.md?chapter=1"><strong>Open the Metadata map</strong></a>, with Chapter 1 highlighted.</p>
<ol>
<li>Select <strong>Metric definition</strong>, then <strong>Example record</strong>. Find the denominator. Does it include unfinished deliveries?</li>
<li>In the <strong>Responsible team</strong> row, select <strong>Delivery Operations</strong> to open its record. What responsibility does this team have?</li>
<li>Return to this chapter using the header’s <strong>Metadata map</strong> button.</li>
</ol>
<p><strong>Think about it:</strong> Does the recorded definition prove that the calculation follows the rule?</p>
<details class="reader-action-answer">
<summary>Check your answer</summary>
<p>The denominator includes <strong>all deliveries due by noon</strong>, including unfinished deliveries. <strong>Delivery Operations</strong> can explain and approve the measure’s meaning. The definition does not prove that the calculation follows it: a reviewer still needs to check the query’s filters and denominator.</p>
</details>
</div>
</aside>
