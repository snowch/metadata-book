# Producing chapter videos

The published videos use the approved Q1 synthetic voice. Start with the
[Q1 production setup](qwen-production/README.md), then use the chapter's
narration, scene plan and rebuild instructions. Keep the source
text and captions unchanged when adjusting how a word is spoken.

## Audit pronunciation after generating narration

Run this step **after `synthesize.py` and before `render.py`**, including after a
pronunciation correction. Install the production requirements first.

```sh
/tmp/qwen-venv/bin/python video/chapter-03/synthesize.py
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-03 --build out/q1-chapter-03
```

The second command extracts every occurrence of the project's `pronunciation`
entries and `pronunciation_review_terms` from the generated speech. It uses
word timings and each engine’s recorded audio offset to extract the complete
term with surrounding context. Qwen timings are estimated by aligning ASR words
to the intended spoken text; they are not provider word boundaries or proof
that every word was spoken. Independent transcription checks are retained
separately.
Whisper transcribes each clip **without vocabulary hints or digit suppression**.
The output is `out/q1-chapter-03/pronunciation-audit/index.html`, with playable clips,
intended speech, unprompted transcription and highlighted differences. A JSON
report records the same findings and hashes the inputs. Working audio and reports
remain in ignored `out/`.

Before synthesis, inspect the script for product names, acronyms, technical terms,
identifiers, dates and percentages. Add unfamiliar terms to
`pronunciation_review_terms`, including terms without a speech override. This is
an explicit review list, not automatic detection of every difficult word.

```json
{
  "pronunciation": {"SQLite": "sequel lite"},
  "pronunciation_review_terms": ["Lineage", "Provenance"]
}
```

Review the pack before spending time on rendering:

1. Check each intended pronunciation. A mistaken override can produce both
   fluent speech and a plausible transcription.
2. Inspect the clips, especially mismatches, missing letters, names and numbers.
   Where listening is available, listen in context. An ASR spelling match alone
   is not approval: it may turn “S Q Lite” into “SQLite”. A mismatch can also be
   a recognition error. Inspect the full passage if an excerpt is ambiguous.
3. Correct the speech mapping, regenerate narration and rerun this audit. Check
   captions and scene cues against the revised timings. Preserve other scene audio.
4. Record the review method and unresolved concerns in the chapter's `review.md`.
   If only automated recognition was available, say so; never claim a listening
   review. A pronunciation that remains uncertain must be labelled unresolved.

Before rendering, confirm the pack still matches the current speech:

```sh
/tmp/qwen-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-03 --build out/q1-chapter-03 --check
EXPLAINER_OUT="$PWD/out/q1-chapter-03" /tmp/qwen-venv/bin/python video/chapter-03/render.py
```

`--check` detects absent or stale reports and changed clips. It does **not**
approve pronunciation or infer that someone listened. Use `--build /path/to/output`
when synthesis used a custom `EXPLAINER_OUT` directory. The default audit model
is `small.en`; weights download on first use.

After rendering, retain the chapter's full narration/content audit, visual checks,
caption checks and browser playback checks. Pronunciation screening does not
replace those checks.

## Page learning aids

The revised chapter videos reinforce a page's central learning task. Use a
concrete demonstration, a prediction/explanation pause, and the existing reader
activity. Long definitions and reference SQL remain available on the page.
`hold_seconds` on a narrated scene adds silent thinking time before the next
scene; captions end with the actual speech. The shared `learning_aid.py` renderer
uses the same Q1 narration and ASR timing contract as the original exports.

After synthesis and pronunciation screening, render the chapter, then run:

```sh
/tmp/qwen-venv/bin/python video/verify_learning_aid.py --chapter 01
# Inspect out/q1-chapter-01/encoded-contact.jpg and the independent scene ASR.
/tmp/qwen-venv/bin/python video/package_learning_aid.py --chapter 01
/tmp/qwen-venv/bin/python scripts/build.py
python video/verify_learning_aid_browser.py --chapter 01
```

The browser check requires Playwright and `/usr/bin/chromium`. Check the actual
encoded frames, response pauses and small-screen readability manually too.
Packaging refreshes this chapter's assets, hashes, duration and provenance only;
it does not deploy. Commit and merge each completed chapter before starting the
next. Record actual review evidence and listening limitations in `review.md`.
