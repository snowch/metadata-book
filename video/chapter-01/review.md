# Chapter 1 Q1 export review — 29 October 2026

The narration now uses the approved original synthetic **Q1 warm British female** voice. The canonical narration, chapter artwork, scene meanings and five-second silent closing card are retained. New passages use the pinned Qwen Base model with one reusable prompt from the approved Q1 reference, rather than a new voice design for each scene.

Export: **2:48**, 1280×720, 24 fps, H.264/yuv420p, AAC and English selectable mov_text captions. There are 50 caption cues; MP4 size is 4,710,935 bytes. SHA-256: `c52d425a02964507c915f31bf3186426e82c8ad0e25ac9c918ebebe5fbbf20ec`. Measured spoken pace is about 161.5 words per minute, including raw passage pauses. The existing project duration bounds pass; no tempo alteration or padding was used to meet them.

## Speech and timing review

All spoken scenes received independent unprompted `small.en` transcription without vocabulary hints or digit suppression. Source ASR text and real timestamps are retained separately from canonical timing metadata. No meaningful omission, wrong number or changed logical distinction was identified in that automated screening.

The pronunciation pack ran after final synthesis and before encoding. It contains 16 contextual clips and 3 transcription differences: three 50.0% clips were recognised as “50 percent”. These are spelling/notation differences consistent with the intended speech. Some short clips contain ASR additions near cut context boundaries; the complete scene transcripts were used to assess meaning. The pack freshness check passed before rendering and again after the resumed exports.

The field passage has an unresolved recognition detail: both unprompted full-passage small.en and an independent base.en recheck write “A column name delivered at…”, while the extracted context clip writes “A column named Delivered At…”. Adjacent /d/ sounds may explain the difference. The field-meaning contrast is retained; no uncertain recognition ending was used to rewrite the speech.

**No human listening review was performed for these new passages.** Recognition cannot certify phonetics, accent or prosody, including a correct-looking term spelling. All pronunciation remains screened rather than listening-approved.

Qwen supplies no word boundaries. Fresh ASR timestamps anchor estimated canonical-word timing; unmatched characters interpolate between adjacent anchors and are marked in `words-NN.json`. Numeric spelling reconciliation does not rewrite original ASR or literal spoken “point”/“zero” words. No old provider timestamps were reused. Captions concatenate exactly to canonical narration, remain ordered and do not overlap; sentence cues follow the new timing.

## Media verification and retained evidence

Full FFmpeg decoding passed. ffprobe confirms the expected video, audio and caption streams. The complete chapter has a five-second silent closing card. Parent independent media/source QC also passed. The parent inspected all actual encoded contact sheets and confirmed staged-site playback, seeking and caption loading at 820px and 390px with no overflow. Posters, actual encoded scene frames and contact sheets are retained alongside each export; the unchanged full-size scene layouts support detailed visual review.

Working evidence is in `out/q1-chapter-01/`: raw/cached speech and generation metadata, independent scene ASR, pronunciation clips/report, timing and caption files, `media-verification.json`, `parent-quality-check.json`, `poster.jpg` and `encoded-frames/`. The [production manifest](../qwen-production/production-manifest.json) retains scene hashes, reference/model provenance, SDK versions, seeds, batch membership, original ASR text and matching coverage. Exact Q1 reference bytes and transcript are retained with production source. Live publication is handled by the publishing workflow.
