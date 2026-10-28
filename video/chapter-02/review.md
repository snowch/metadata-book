# Chapter 2 export review — 28 October 2026

Export: **3:52**, 1280×720, 24 fps, ten scenes, 62 selectable caption cues and a five-second silent closing card. MP4 size: 6,160,306 bytes. SHA-256: `fe1591ff90598deabff1d9f1be29181c706470ca33909d85cc41983c562d44fd`.

## Content and visuals

The narration was reviewed against Chapter 2 and the executable delivery example before synthesis. It preserves the declared-type caveat, required-value flags and primary key, the complete-record assumption for NULL, the original-versus-revised promise, view recalculation on reading, both denominators, fixed UTC text assumption, query-versus-output distinction and overlapping catalogue roles.

The complete eleven-line view in the renderer matches `examples/deliveries.sql` exactly. Executing that source confirms the displayed column metadata, four delivery rows and completed result `(3, 2, 66.7)`. The all-due comparison is 2/4 = 50.0%. The timeline labels 12:30 as the revised promised deadline, not the time the revision occurred.

Static previews and actual encoded frames from all ten scenes were inspected, including full-size column records and SQL. No clipped text or overlapping elements were found. The full SQL uses 24px monospaced type; the narration explains its key steps without reading identifiers aloud. The filter highlight follows its sentence cue. All other main content uses larger type. Source, script and visual checks were performed separately from automated audio recognition.

## Pronunciation and speech

A short voice sample covered SQLite, schema, primary key, NULL, both percentages, UTC and the catalogue names. Unprompted `small.en` recognition returned the intended names and values. Speech explicitly maps SQLite to “sequel lite”, 66.7% to “sixty six point seven percent” and 50.0% to “fifty percent”.

The shared pronunciation audit ran **after synthesis and before encoding**, covering 24 technical-term occurrences. It used no vocabulary hints or digit suppression. Three text differences were inspected: two SQLite clips were written as “sequel light” and 50.0% as “50%”. Those recognised forms are consistent with the intended speech, but they do not establish a phonetic approval. No other term mismatches were flagged. The audit freshness check passed before rendering.

The full track was transcribed without hints using `base.en`. Isolated `small.en` checks of the opening, saved-query scene and recap investigated omitted text and boundary repetitions. The isolated saved-query check includes the sentence that the view calculates its result whenever it is read. Recognition paraphrased “query those descriptions” as “query them”; provider word alignment still matches the complete submitted script. No speech was changed solely to force an ASR spelling match.

**No human listening review was performed.** Pronunciation and prosody remain screened by automated recognition rather than listening. The original speech, provider boundaries, voice preview and audit clips are retained under ignored `out/chapter-02/` for inspection.

## Export and embedding

- Provider word-boundary alignment passed. The 62 ordered, non-overlapping caption cues concatenate exactly to the canonical narration.
- ffprobe confirms H.264/yuv420p, 24 fps, AAC at 48 kHz and English mov_text captions. Video duration is 232.208333 seconds; audio/container is 232.3 seconds. Full FFmpeg decoding passed.
- The embedded player passed Chromium checks at 320, 768 and 1024 pixels in light and dark themes: no overflow or initial MP4 request, no autoplay, all 62 WebVTT cues load, seeking and playback work, and the player is hidden in print.
- The complete source SQL, pronunciation regression tests, SQLite examples, map records/layout, book build and local links passed.

Source and production settings are in `video/chapter-02/`. Final MP4, poster, WebVTT captions and transcript are published under `assets/video/chapter-02/`. Working audio, scene clips, timings, previews and audit reports remain outside git. The player identifies the invented example and synthetic narration.
