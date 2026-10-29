# Chapter 7 page learning aid

Choose a measure by its denominator and explain why passed input checks do not establish a ready report publication.

`narration.json` is the exact authored script; `scene-plan.md` records the source,
learning task and visual guards. Use the approved original Q1 voice and
[Qwen production environment](../qwen-production/README.md), following the explainer
repository's [Qwen guidance](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/qwen-speech.md)
and [learning-aid criteria](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/learning-aid-criteria.md).

Run from the repository root:

```sh
/tmp/qwen-venv/bin/python video/chapter-07/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-07 --build out/q1-chapter-07
# Inspect full-scene ASR, pronunciation excerpts and unresolved questions.
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-07 --build out/q1-chapter-07 --check
/tmp/qwen-venv/bin/python video/chapter-07/render.py
/tmp/qwen-venv/bin/python video/verify_learning_aid.py --chapter 07
# Inspect actual encoded frames, staged reveals, holds and phone rendering.
/tmp/qwen-venv/bin/python video/package_learning_aid.py --chapter 07
/tmp/qwen-venv/bin/python scripts/build.py
python video/verify_learning_aid_browser.py --chapter 07
```

Working evidence stays in ignored `out/q1-chapter-07/`. Keep raw audio and hashes,
independent ASR, estimated alignment, pronunciation reports, captions and clips
for corrections. The two four-second response holds follow complete question
speech and captions. Explicit packaging adds the page embed and manifest entry;
publication follows the agreed commit/merge workflow, with deployed files checked.
See `review.md` for actual checks and limitations. Recognition is not a listening
review; retention/transfer need separate reader evidence.
