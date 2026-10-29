"""Single whole-passage Nano audition, CPU, packaged default voice, no reference."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
for name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[name] = "2"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import hashlib
from importlib.metadata import version
import json
import resource
import subprocess
import time
from datetime import datetime, timezone
import numpy as np
import soundfile as sf
import torch
from chatterbox.tts_turbo import ChatterboxTurboTTS, punc_norm

TEXT = ("The column records describe three fields: a delivery identifier, a promise time, "
        "and a delivery time. All three declare text. In this sequel lite table, that "
        "declaration does not strictly enforce the type of every stored value. The not-null "
        "flag is one for the identifier and promise: a value is required. Zero for delivery "
        "time allows null, the marker for a missing value. The primary key uniquely "
        "identifies each row. Here, the delivery identifier is the sole key.")
SETTINGS = dict(repetition_penalty=1.2, min_p=0.0, top_p=0.95,
                audio_prompt_path=None, exaggeration=0.0, cfg_weight=0.0,
                temperature=0.8, top_k=1000, norm_loudness=True)
SEED = 20261029
torch.set_num_threads(2)
torch.set_num_interop_threads(2)
torch.manual_seed(SEED)
np.random.seed(SEED)
(ROOT / "spoken-text.txt").write_text(TEXT + "\n")
(ROOT / "provider-normalized-text.txt").write_text(punc_norm(TEXT) + "\n")
manifest = json.loads((ROOT / "download-manifest.json").read_text())
metadata = {
    "started_at": datetime.now(timezone.utc).isoformat(),
    "repository": manifest["repository"], "revision": manifest["revision"],
    "weights_license": manifest["license"], "code_license": "MIT",
    "code_repository": "https://github.com/resemble-ai/chatterbox",
    "code_revision": subprocess.check_output(["git", "-C", str(ROOT / "source"), "rev-parse", "HEAD"], text=True).strip(),
    "voice": "Model-packaged default conditionals from pinned conds.pt; no reference recording",
    "input_text": TEXT, "provider_normalized_text": punc_norm(TEXT),
    "punctuation_note": "Upstream punc_norm changes colons to commas; input words unchanged; actual speech requires review",
    "request_unit": "one complete passage", "device": "cpu",
    "torch_threads": torch.get_num_threads(), "seed": SEED,
    "settings": SETTINGS,
    "versions": {name: version(name) for name in ["chatterbox-tts", "torch", "torchaudio", "transformers", "numpy", "soundfile", "resemble-perth"]},
    "quality_review": "No listening or pronunciation approval asserted; parent audits final sample",
}
start = time.perf_counter()
print("Loading pinned Nano model on CPU", flush=True)
model = ChatterboxTurboTTS.from_local(ROOT / "model", device="cpu", nano=True)
metadata["load_seconds"] = time.perf_counter() - start
assert model.conds is not None, "Packaged default voice absent; no unapproved reference may be used"
sampling = {}
original = model.t3.inference_turbo

def instrumented(*args, **kwargs):
    sampling["maximum_generation_tokens"] = kwargs.get("max_gen_len", 1000)
    result = original(*args, **kwargs)
    sampling["generated_tokens_after_eos_removal"] = int(result.shape[-1])
    return result

model.t3.inference_turbo = instrumented
print("Generating whole passage with model-packaged voice", flush=True)
start = time.perf_counter()
with torch.inference_mode():
    wav = model.generate(TEXT, **SETTINGS)
metadata["generation_seconds"] = time.perf_counter() - start
audio = wav.squeeze().detach().cpu().numpy()
assert audio.ndim == 1 and audio.size and np.isfinite(audio).all()
path = ROOT / "sample-nano.wav"
# Preserve the exact returned floating waveform; parent makes loudness-matched copies.
sf.write(path, audio, model.sr, subtype="FLOAT")
alias = ROOT / "sample.wav"
if not alias.exists():
    alias.symlink_to(path.name)
metadata.update({
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "file": path.name, "sha256": hashlib.file_digest(path.open("rb"), "sha256").hexdigest(),
    "sample_rate": model.sr, "channels": 1, "sample_format": "32-bit float WAV",
    "frames": int(audio.size), "duration_seconds": float(audio.size / model.sr),
    "peak_absolute_amplitude": float(np.max(np.abs(audio))),
    "sampling": sampling,
    "generation_limit_reached": sampling["generated_tokens_after_eos_removal"] >= sampling["maximum_generation_tokens"],
    "peak_process_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "watermark": "Official Chatterbox PerTh watermark preserved",
    "postprocessing": "No silence trimming, padding, time stretch, or loudness change added by trial script",
})
(ROOT / "sample-nano.metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps({k: metadata[k] for k in ["file", "duration_seconds", "load_seconds", "generation_seconds", "generation_limit_reached", "peak_process_rss_kib"]}), flush=True)
if metadata["generation_limit_reached"]:
    raise RuntimeError("Generation hit upstream token limit; saved sample requires completeness investigation")
