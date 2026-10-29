# Chapter 4 page learning aid

Reinforces [Why is this report out of date?](../../chapters/04-outdated-reports.md):
explain the stale output and verify that recovery reaches the report. The
existing map intentionally contains earlier records; recovery is checked against
the page's later publication/refresh table. `scene-plan.md` records source and
visual interpretation guards; `narration.json` is the exact authored narration.

Use the approved Q1 voice and existing CPU environment from
[Q1 production](../qwen-production/README.md). Follow the explainer repository's
[Qwen guide](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/qwen-speech.md)
and [learning-aid criteria](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/learning-aid-criteria.md).

From the repository root:

```sh
/tmp/qwen-venv/bin/python video/chapter-04/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-04 --build out/q1-chapter-04
# Inspect full-scene ASR and pronunciation excerpts; record review limitations.
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-04 --build out/q1-chapter-04 --check
/tmp/qwen-venv/bin/python video/chapter-04/render.py
/tmp/qwen-venv/bin/python video/verify_learning_aid.py --chapter 04
# Inspect actual encoded frames and phone rendering before packaging.
/tmp/qwen-venv/bin/python video/package_learning_aid.py --chapter 04
/tmp/qwen-venv/bin/python scripts/build.py
python video/verify_learning_aid_browser.py --chapter 04
```

Outputs stay in ignored `out/q1-chapter-04/` until explicit packaging. Preserve
raw speech, provenance, ASR originals, estimated alignment, captions and clips for
revisions. The two `hold_seconds` values add four seconds after complete question
speech and captions, before answer scenes. New chapters are added to the page
and production manifest by packaging; it does not publish. Merge this chapter
before starting the next, then verify the published media and captions.

See `review.md` for actual evidence. Recognition is not a human listening review;
retention/transfer outcomes remain unassessed without reader observations.
