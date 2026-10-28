# Producing chapter videos

Use the chapter's narration, scene plan and rebuild instructions. Keep the source
text and captions unchanged when adjusting how a word is spoken.

## Audit pronunciation after generating narration

Run this step **after `synthesize.py` and before `render.py`**, including after a
pronunciation correction. Install the chapter's `requirements-audit.txt` first.

```sh
/tmp/metadata-video-venv/bin/python video/chapter-03/synthesize.py
/tmp/metadata-video-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-03
```

The second command extracts every occurrence of the project's `pronunciation`
entries and `pronunciation_review_terms` from the generated speech. It uses
provider word timings to preserve the complete term with surrounding context.
Whisper transcribes each clip **without vocabulary hints or digit suppression**.
The output is `out/chapter-03/pronunciation-audit/index.html`, with playable clips,
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
/tmp/metadata-video-venv/bin/python video/audit_pronunciation.py --chapter video/chapter-03 --check
/tmp/metadata-video-venv/bin/python video/chapter-03/render.py
```

`--check` detects absent or stale reports and changed clips. It does **not**
approve pronunciation or infer that someone listened. Use `--build /path/to/output`
when synthesis used a custom `EXPLAINER_OUT` directory. The default audit model
is `small.en`; weights download on first use.

After rendering, retain the chapter's full narration/content audit, visual checks,
caption checks and browser playback checks. Pronunciation screening does not
replace those checks.
