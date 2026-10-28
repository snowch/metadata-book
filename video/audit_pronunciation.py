"""Build an unprompted pronunciation-review pack from generated scene audio.

Transcription is a screening aid, never proof of pronunciation. Requires the
chapter's requirements-audit.txt; --check uses only the Python standard library.
"""
import argparse
import bisect
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import wave


def normalise(text):
    return ''.join(c.lower() for c in text if c.isalnum())


def pattern(terms, flags=0):
    return re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(t) for t in
                      sorted(terms, key=len, reverse=True)) + r')(?!\w)', flags)


def spoken(text, lexicon):
    return pattern(lexicon).sub(lambda m: lexicon[m[0]], text) if lexicon else text


def occurrences(text, words, lexicon, review_terms):
    """Map canonical terms to provider word ranges, including multiword aliases."""
    terms = set(lexicon) | set(review_terms)
    if not terms:
        return []
    starts, ends, joined = [], [], ''
    for word in words:
        starts.append(len(joined))
        joined += normalise(word['text'])
        ends.append(len(joined))
    if joined != normalise(spoken(text, lexicon)):
        raise ValueError('Word boundaries do not match the current pronunciation settings; regenerate speech.')
    result = []
    for match in pattern(terms, re.IGNORECASE).finditer(text):
        before = len(normalise(spoken(text[:match.start()], lexicon)))
        intended = spoken(match[0], lexicon)
        after = before + len(normalise(intended))
        first = bisect.bisect_right(ends, before)
        last = bisect.bisect_left(ends, after)
        result.append((match[0], intended, first, last))
    return result


def fingerprint(chapter, build):
    scenes = json.loads((chapter / 'narration.json').read_text())
    paths = [chapter / 'project.json', chapter / 'narration.json', build / 'timings.json']
    paths += [build / name for i, scene in enumerate(scenes) if scene['text']
              for name in (f'audio-{i:02}.wav', f'words-{i:02}.json')]
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    for path in paths:
        digest.update(path.name.encode())
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def write_html(report, destination):
    esc = html.escape
    cards = []
    for item in report['terms']:
        status = 'Text recognised — pronunciation still needs review' if item['text_match'] else 'Inspect this clip — transcription differs'
        card_class = '' if item['text_match'] else 'mismatch'
        cards.append(f'''<section class="{card_class}"><h2>{esc(item['term'])}</h2>
<p>Scene {item['scene'] + 1} · chapter time {item['chapter_time']:.1f}s</p>
<p><strong>Intended speech:</strong> {esc(item['intended'])}</p>
<audio controls preload="none" src="{esc(item['clip'])}"></audio>
<p><strong>Unprompted transcription:</strong> {esc(item['recognised']) or '(no speech recognised)'}</p>
<p class="status">{status}</p></section>''')
    destination.write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pronunciation review</title><style>
body{max-width:850px;margin:2rem auto;padding:0 1rem;background:#f7f4ed;color:#292d29;font:17px/1.6 system-ui}
h1,h2{font-family:Georgia,serif}section{background:#fffdf8;border:1px solid #ddd8cd;padding:1rem 1.5rem;margin:1rem 0;border-radius:10px}
audio{width:100%}.status{color:#96432e;font-weight:600}.mismatch{border-left:4px solid #96432e}
</style><h1>Pronunciation review</h1>
<p>Listen to each term in context and compare it with the intended speech.
Recognition used no vocabulary prompt or digit suppression. A correct spelling
can conceal a spoken error; a mismatch can also be a transcription error.</p>
<p>These clips are excerpts. Boundary words may be cut. This pack does not certify
pronunciation, and it covers only the terms listed in the project settings.
Also inspect the complete narration for omitted terms, names and acronyms.</p>
''' + '\n'.join(cards) + '</html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter', required=True, type=Path, help='Source directory, e.g. video/chapter-03')
    parser.add_argument('--build', type=Path, help='Default: out/<chapter directory name>')
    parser.add_argument('--model', default='small.en')
    parser.add_argument('--check', action='store_true', help='Check that the review pack matches current inputs; does not certify pronunciation')
    args = parser.parse_args()
    chapter = args.chapter.resolve()
    build = (args.build or Path(__file__).resolve().parents[1] / 'out' / chapter.name).resolve()
    dest = build / 'pronunciation-audit'
    report_path = dest / 'report.json'
    current = fingerprint(chapter, build)
    if args.check:
        report = json.loads(report_path.read_text())
        if report['input_fingerprint'] != current:
            raise ValueError('Pronunciation audit is stale; regenerate it after speech or configuration changes.')
        for entry in report['terms']:
            if hashlib.sha256((dest / entry['clip']).read_bytes()).hexdigest() != entry['clip_sha256']:
                raise ValueError('Review clip changed; regenerate the audit.')
        print('Pronunciation pack matches current inputs. This is not a pronunciation approval.')
        return

    import numpy as np
    from faster_whisper import WhisperModel

    config = json.loads((chapter / 'project.json').read_text())
    scenes = json.loads((chapter / 'narration.json').read_text())
    timings = json.loads((build / 'timings.json').read_text())
    if [s['text'] for s in scenes] != [t['text'] for t in timings]:
        raise ValueError('Narration and timings differ; regenerate speech.')
    dest.mkdir(parents=True, exist_ok=True)
    # Invalidate the previous pack before replacing clips, so an interrupted run
    # cannot be mistaken for a completed audit.
    report_path.unlink(missing_ok=True)
    model = WhisperModel(args.model, device='cpu', compute_type='int8', cpu_threads=2)
    entries = []
    for i, scene in enumerate(scenes):
        if not scene['text']:
            continue
        words = json.loads((build / f'words-{i:02}.json').read_text())['words']
        found = occurrences(scene['text'], words, config.get('pronunciation', {}),
                            config.get('pronunciation_review_terms', []))
        # synthesize.py trims first offset minus 80 ms and adds 250 ms lead-in.
        shift = .25 - max(0, words[0]['offset'] / 1e7 - .08)
        with wave.open(str(build / f'audio-{i:02}.wav'), 'rb') as wav:
            params = wav.getparams()
            data = wav.readframes(wav.getnframes())
        frame_size = params.nchannels * params.sampwidth
        duration = params.nframes / params.framerate
        for term, intended, first, last in found:
            start = words[first]['offset'] / 1e7 + shift
            finish = (words[last]['offset'] + words[last]['duration']) / 1e7 + shift
            if start < 0 or finish > duration:
                raise ValueError('Term lies outside the audio; regenerate speech.')
            begin, end = max(0, start - 1.2), min(duration, finish + 1.2)
            filename = f'term-{len(entries):03}.wav'
            clip = dest / filename
            with wave.open(str(clip), 'wb') as wav:
                wav.setparams(params)
                wav.writeframes(data[round(begin * params.framerate) * frame_size:
                                     round(end * params.framerate) * frame_size])
            decoded = subprocess.check_output(['ffmpeg', '-hide_banner', '-loglevel', 'error',
                         '-i', str(clip), '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'])
            segments, _ = model.transcribe(np.frombuffer(decoded, dtype=np.float32),
                         language='en', beam_size=5, condition_on_previous_text=False,
                         initial_prompt=None, suppress_tokens=[-1], vad_filter=True)
            recognised = ' '.join(segment.text.strip() for segment in segments)
            # A spelling match is deliberately not a pronunciation verdict.
            matches = any(normalise(value) in normalise(recognised) for value in (term, intended))
            entries.append(dict(term=term, intended=intended, scene=i,
                         chapter_time=timings[i]['start'] + start, clip=filename,
                         clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),
                         recognised=recognised, text_match=matches,
                         pronunciation_verified=False))
            print(f'{term}: {recognised or "(no speech recognised)"}', flush=True)
    if not entries:
        raise ValueError('No review terms found. Add technical terms or pronunciations to project.json.')
    report = dict(input_fingerprint=current, model=args.model, vocabulary_prompt=None,
                  digit_suppression=False, pronunciation_verified=False, terms=entries)
    write_html(report, dest / 'index.html')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Review {len(entries)} clips at {dest / "index.html"}; '
          f'{sum(not e["text_match"] for e in entries)} transcription differences. '
          'No pronunciation approval is inferred.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileNotFoundError) as error:
        raise SystemExit(str(error)) from error
