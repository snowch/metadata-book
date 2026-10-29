# Chapter 6 page learning aid

Explain why duplicate, delayed, missing and conflicting records need different evidence before changing current state.

`narration.json` is the exact authored script; `scene-plan.md` records the source,
learning task and visual guards. Use the approved original Q1 voice and
[Qwen production environment](../qwen-production/README.md), following the explainer
repository's [Qwen guidance](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/qwen-speech.md)
and [learning-aid criteria](https://github.com/snowch/explainer-video-generator/blob/f16d0350df20cb35681886cb5d197ce27f2d3a49/docs/learning-aid-criteria.md).

Run from the repository root:

```sh
/tmp/qwen-venv/bin/python video/chapter-06/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-06 --build out/q1-chapter-06
# Inspect full-scene ASR, pronunciation excerpts and unresolved questions.
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-06 --build out/q1-chapter-06 --check
/tmp/qwen-venv/bin/python video/chapter-06/render.py
/tmp/qwen-venv/bin/python video/verify_learning_aid.py --chapter 06
# Inspect actual encoded frames, staged reveals, holds and phone rendering.
/tmp/qwen-venv/bin/python video/package_learning_aid.py --chapter 06
/tmp/qwen-venv/bin/python scripts/build.py
python video/verify_learning_aid_browser.py --chapter 06
```

Working evidence stays in ignored `out/q1-chapter-06/`. Keep raw audio and hashes,
independent ASR, estimated alignment, pronunciation reports, captions and clips
for corrections. The two four-second response holds follow complete question
speech and captions. Explicit packaging adds the page embed and manifest entry;
publication follows the agreed commit/merge workflow, with deployed files checked.
See `review.md` for actual checks and limitations. Recognition is not a listening
review; retention/transfer need separate reader evidence.
