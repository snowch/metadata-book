"""Offline regression checks for pronunciation clip selection and audit freshness."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from audit_pronunciation import audio_time_shift, fingerprint, occurrences


def words(text):
    return [{'text': word, 'offset': i * 10000000, 'duration': 5000000}
            for i, word in enumerate(text.split())]


class PronunciationAuditTests(unittest.TestCase):
    def test_explicit_padding_overrides_legacy_provider_trim(self):
        record = {'words': [{'offset': 5000000}], 'audio_time_offset_seconds': .25}
        self.assertEqual(audio_time_shift(record), .25)
        del record['audio_time_offset_seconds']
        self.assertAlmostEqual(audio_time_shift(record), -.17)

    def test_invalid_explicit_offsets_are_rejected(self):
        for value in (float('nan'), float('inf'), '0.25', True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                audio_time_shift({'audio_time_offset_seconds': value})

    def test_sqlite_override_covers_both_spoken_words(self):
        result = occurrences('Using SQLite now.', words('Using sequel lite now'),
                             {'SQLite': 'sequel lite'}, [])
        self.assertEqual(result, [('SQLite', 'sequel lite', 1, 2)])

    def test_old_speech_is_rejected_after_mapping_fix(self):
        with self.assertRaisesRegex(ValueError, 'regenerate speech'):
            occurrences('Using SQLite now.', words('Using S Q Lite now'),
                        {'SQLite': 'sequel lite'}, [])

    def test_overlapping_run_ids_are_not_double_counted(self):
        result = occurrences('summary-R1205 uses R1205.',
                             words('summary R twelve oh five uses R twelve oh five'),
                             {'R1205': 'R twelve oh five',
                              'summary-R1205': 'summary R twelve oh five'}, [])
        self.assertEqual([(x[0], x[2], x[3]) for x in result],
                         [('summary-R1205', 0, 4), ('R1205', 6, 9)])

    def test_unmapped_review_term_is_included_without_substring_match(self):
        result = occurrences('Provenance and provenance, not provenanceish.',
                             words('Provenance and provenance not provenanceish'), {}, ['Provenance'])
        self.assertEqual(result, [('Provenance', 'Provenance', 0, 0),
                                 ('provenance', 'provenance', 2, 2)])

    def test_check_rejects_changed_audio_and_clips(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            chapter, build = root / 'chapter', root / 'out'
            chapter.mkdir(); build.mkdir()
            (chapter / 'project.json').write_text('{}')
            (chapter / 'narration.json').write_text('[{"text":"SQLite"}]')
            (build / 'timings.json').write_text('[]')
            (build / 'words-00.json').write_text('{}')
            audio = build / 'audio-00.wav'
            audio.write_bytes(b'original audio')
            pack = build / 'pronunciation-audit'; pack.mkdir()
            clip = pack / 'term-000.wav'; clip.write_bytes(b'original clip')
            report = {'input_fingerprint': fingerprint(chapter, build), 'terms': [
                {'clip': clip.name, 'clip_sha256': hashlib.sha256(clip.read_bytes()).hexdigest()}]}
            (pack / 'report.json').write_text(json.dumps(report))
            command = [sys.executable, str(Path(__file__).with_name('audit_pronunciation.py')),
                       '--chapter', str(chapter), '--build', str(build), '--check']
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            audio.write_bytes(b'regenerated audio')
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('stale', result.stderr)
            audio.write_bytes(b'original audio'); clip.write_bytes(b'changed clip')
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('clip changed', result.stderr)


if __name__ == '__main__':
    unittest.main()
