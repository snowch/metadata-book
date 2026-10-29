# Chapter 6 scene plan

Audience: report readers and engineers. Embedded page aid. Source: chapters/06-unreliable-records.md at f8bb703316888ca0fcdb78d728e0f0b5381bbb18. Guidance: explainer f16d0350df20cb35681886cb5d197ce27f2d3a49.
Objective: Explain why duplicate, delayed, missing and conflicting records need different evidence before changing current state.
Takeaway: preserve each claim and show what remains uncertain.

| Scene | Visual / source | Interpretation guard |
|---|---|---|
| missing-question | Yesterday seen / today absent; question, 4s hold | No deletion or answer shown |
| missing-answer | Last observation retained; unverified current status | Confirm deletion needs scope, permission and outcome evidence |
| repeat | E20 received 10:01 and 10:04; second receipt enters later | One reported event, not proven physical publication; source plus stable ID |
| late | E19 event 09:50 / receipt 10:06; earlier history | Different run; timestamps not universal cross-system ordering |
| conflict-question | E20 reports summary-R1000 at 10:00; S7 observes summary-R0940 at 10:03 | No winner or explanation revealed during 4s hold |
| conflict-answer | Both claims retained; disputed state | Neither source proved correct; duplicate handling cannot settle conflict |
| investigate | Evidence → recorded conclusion | Write logs/saved versions are checks, not already supplied proof |
| practice | Map Source observation / Collection run, 20 Oct | Distinguish map from 21 Oct events; map contains no later deletion record |
| end | 5s page practice card | No new claim |

Exact narration: narration.json. Short evidence excerpts; full records remain on page. Two four-second silent holds follow completed questions and captions. ASR timings are estimates. Inspect actual encoded reveals, phone view, captions and playback; no human listening or learner-outcome claim.
