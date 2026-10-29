"""Download only the pinned public Nano files used by the official CPU loader."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import shutil
import urllib.request

ROOT = Path(__file__).resolve().parent
REPO = "ResembleAI/chatterbox-nano"
REVISION = "71ccd1d0081b430592cea481f4307e764e07bc64"
FILES = ["README.md", "conds.pt", "s3gen_meanflow.safetensors",
         "t3_nano_v1.safetensors", "ve.safetensors", "added_tokens.json",
         "merges.txt", "special_tokens_map.json", "tokenizer_config.json",
         "vocab.json", "t3_nano_v1.yaml"]
DEST = ROOT / "model"
DEST.mkdir(exist_ok=True)

def open_url(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "metadata-book-voice-trial/1.0"}), timeout=120)

with open_url(f"https://huggingface.co/api/models/{REPO}/revision/{REVISION}?blobs=true") as response:
    info = json.load(response)
(ROOT / "model-card-metadata.json").write_text(json.dumps(info, indent=2) + "\n")
expected = {item["rfilename"]: item for item in info["siblings"]}

def download(name):
    path = DEST / name
    item = expected[name]
    digest = item.get("lfs", {}).get("sha256")
    size = item.get("size", item.get("lfs", {}).get("size"))
    if not path.exists() or (size and path.stat().st_size != size):
        temporary = path.with_name(path.name + ".partial")
        with open_url(f"https://huggingface.co/{REPO}/resolve/{REVISION}/{name}") as response, temporary.open("wb") as out:
            shutil.copyfileobj(response, out, length=4 * 1024 * 1024)
        os.replace(temporary, path)
    actual = hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
    if digest and actual != digest:
        raise RuntimeError(f"Checksum failed for {name}")
    if size and path.stat().st_size != size:
        raise RuntimeError(f"Size check failed for {name}")
    print(f"Verified {name}: {path.stat().st_size} bytes", flush=True)
    return {"file": name, "bytes": path.stat().st_size, "sha256": actual, "lfs_sha256_verified": bool(digest)}

with ThreadPoolExecutor(max_workers=2) as pool:
    files = list(pool.map(download, FILES))
(ROOT / "download-manifest.json").write_text(json.dumps({"repository": REPO, "revision": REVISION, "license": info.get("cardData", {}).get("license"), "files": files}, indent=2) + "\n")
