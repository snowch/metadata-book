# Chapter 1 replacement review — 10 November 2026

Audience: engineers who can read a table, new to judging metric definitions.
Objective: choose a population, explain inclusion of unfinished deliveries, and
check the query against the chosen definition. Source and production hashes:
`production.json`. The six-parcel problem is a separate invented example.

## Design and learning review

Applied the Frontend Design skill (anthropics/skills, skills/frontend-design),
Cognitive Load Analyser and Worked Example Fading skills
(GarethManning/education-agent-skills, memory-learning-science). The recording
workflow is snowch/claude-skills record-demo, with its tested Linux adapter.

The initial source review found repetitive slide chrome, mostly static fades
and small labels. The replacement uses one persistent diagram, a stable numerator,
a visible change in denominator membership and a distinct practice example.
The indigo/teal/slate palette and Source Sans typography connect the page, lab,
PDF and recording. Status labels accompany colours. Motion has a reduced-motion
alternative in the learner-facing lab. Full definitions remain in the lesson.

The worked example explains why the late parcel counts as completed. The guided
question retains the unfinished parcel outside that group until the answer.
The six-parcel problem changes the result to 33.3%; choosing four receives feedback
explaining that it counts completed deliveries. Both question recordings leave
five seconds after speech. Users can pause or work independently in the lab.
Experienced readers can go directly to the six-parcel exercise.

## Visual correction after screenshot review

The earlier recording still showed too many simultaneous labels, and the page
squeezed its landscape player beside the navigation. This revision removes the
recording header, repeated context, timestamps, grouping line and explanation
paragraph. Each scene keeps one heading and a larger labelled diagram. The
calculation appears at its spoken cue; the bottom 20% stays clear for controls
and captions. Six parcels use two rows, retaining readable labels.

The player now uses more of the page width. Navigation collapses below 1200px;
on a 390px screen the video spans the full 390px. At 960px and 1280px viewport
widths the player measures 915px and 1005px. The embedded lab reports its content
height as exercises change, removing the fixed blank area above the video.

Native browser renders follow the retained 2785-frame timeline. Audio and
subtitle packet hashes, presentation timestamps and durations exactly match the
previous published recording. No speech or caption timing was regenerated.
Actual encoded frames before and after calculation reveals were inspected;
mobile/tablet/desktop checks cover frame resizing, practice feedback and overflow.
The PDF and poster use the same simplified composition.

## Speech and media evidence

92.833 seconds; native 3840×2160 at 30 fps. The silent master shares the picture
with the narrated version. No frame upscaling. Full canonical captions, transcript,
PDF deck and timecoded shot list retained. Raw audio and original independent ASR
remain in ignored out/chapter-01-v2/.

Eight passages use the skill's af_heart synthetic voice on CPU. Independent
Whisper preserved the script's numbers and qualifications. Its initial two
similarity flags are number-word/numeral formatting (50% and 33.3%), not evidence
of changed arithmetic. Fresh word-level ASR aligned to the canonical script at
100% normalized character coverage in all eight scenes; caption timing is estimated.
Native capture reported no problems, no leaks and all frames at 3840×2160.

No human listening review was performed. Phoneme inspection, level/pace screening
and ASR do not certify expressive delivery or precise phonetics. Reader learning,
delayed recall and transfer outcomes remain unassessed. These are design and
technical findings, not measured learning gains.

## Verification

- Full FFmpeg decode and native media dimensions/frame rate.
- Exact original/new audio and subtitle packet equality; 2785 video frames retained.
- All eight recording scenes fit above the 144px control/caption safe area.
- At 390px, 960px and 1280px: lab height grows and shrinks with content, no horizontal overflow, responsive player and navigation.
- Caption text exactly matches the approved narration.
- Exported audio is silent in both question response windows; no active captions.
- Actual encoded frames and response holds inspected separately from deck exports.
- Lab at 390px and 960px: correct 66.7%/50.0% groups, hidden six-parcel answer, and explanatory feedback for denominator four.
- Lesson/player at 390px and 1280px: playback, captions, seeking, lab feedback, completion marks and star header.
- Full site/link build, existing examples, map data/layout validation and pronunciation tests.

Free space before starting Chapter 1: 26 GB. Other chapter recordings are unchanged.
