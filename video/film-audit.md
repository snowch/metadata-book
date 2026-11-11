# Lesson film audit — November 2026

Audience: engineers who can read tables and queries, learning to assess metadata
evidence. These films reinforce the chapter's task; the page retains definitions,
full SQL, reference records and independent activities.

## Criteria

| Criterion | Evidence to inspect |
|---|---|
| Relevance and accuracy | Match the example, rule, scope and qualifications on the chapter page. |
| Engagement | Start with a concrete decision; make a meaningful change visible. |
| Attention and readability | One heading and one focal diagram; remove repeated chrome and prose. |
| Pacing and explanation | Reveal evidence as discussed; keep question answers out of response holds. |
| Memorability | Reuse a stable visual relationship and finish with a short retrieval cue. |
| Practice and transfer | Preserve prediction/explanation pauses and return to the page's map activity. |
| Accessibility | Captions and transcript, labels alongside colour, control-safe area, responsive player. |
| Media integrity | Decode encoded export, inspect actual frames, exercise playback and seeking. |
| Speech integrity | Copy approved speech and caption packets unchanged for picture-only work. |

Applied [Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design),
[Cognitive Load Analyser](https://github.com/GarethManning/education-agent-skills/tree/main/skills/memory-learning-science/cognitive-load-analyser)
and [Worked Example Fading](https://github.com/GarethManning/education-agent-skills/tree/main/skills/memory-learning-science/worked-example-fading-designer).
The native browser/deck export follows the Linux-compatible
[record-demo workflow](https://github.com/snowch/claude-skills/tree/main/plugins/demo-video/skills/record-demo).
The existing approved Q1 speech is retained; this does not change to Kokoro.

## Design plan and critique

Use Chapter 1's parcel/evidence visual language: paper `#fafcff`, ink `#172635`,
indigo `#3657d6`, teal `#087d79`, muted ink `#4a6072`, and rule `#cbd9e6`.
Source Sans 3 carries headings and diagram labels. The diagram, rather than
decorative slide chrome, is the memorable element. Layout is centred for
comparisons and left-aligned for labelled records. No repeated chapter banner,
subtitle or explanatory footer; bottom 144 of 720 layout pixels stay empty.

The older uniform stack of cards creates redundancy and split attention, with
important conclusions near controls. Simply enlarging those cards would retain
the problem. Instead, use parcel membership, matched identifiers, timelines,
source-labelled claims and purposeful comparisons; sequence dense explanations
into separate states. Persistent labels supply the facts needed to reason, while
speech explains their relationships. Questions retain productive difficulty.

Intrinsic complexity remains: different timestamps, identities, evidence scopes
and business rules must still be distinguished. The design reduces presentation
load, not those distinctions. Existing guided questions and independent page
activities are preserved; this is not a newly validated complete fading curriculum.
Experienced readers can skip to the map activity or transcript. No observed
learning gains, delayed recall, transfer results or human listening approval are
claimed. Each chapter's review records concrete changes and completed checks.

## Rebuild a revised film

With Playwright, Pillow, pypdf, FFmpeg and Chromium installed:

```sh
python video/lesson_film.py --chapter 02 --preview
# Inspect out/q1-chapter-02/film-preview.jpg and the authored film.json.
python video/lesson_film.py --chapter 02 --package
python scripts/build.py
python video/verify_learning_aid_browser.py --chapter 02
```

`film.json` is the current picture source; the old Pillow `render.py` remains as
the original production source. Published narration, subtitle text and timing
are unchanged. `before-film-audit.mp4` under ignored `out/` preserves the original
export; retain it. Exact scene boundaries are recovered from retained generation
durations and the original 24fps padding contract, then checked against the
original frame count and captions. Caption cue boundaries anchor later diagram
states; these are estimates inherited from the original caption alignment.

The browser renders native 3840×2160 states and a vector PDF of all states,
including questions before answers. Exports include narrated and silent masters,
captions, transcript, poster, PDF and a timecoded production manifest. Font bounds,
label overlaps and the control-safe area are checked before encoding. The media
verifier checks the encoded output and silent response windows; inspect extracted
encoded frames separately. Packaging updates only the selected chapter. Merge
each completed chapter and check `df -h /workspace` before the next.
