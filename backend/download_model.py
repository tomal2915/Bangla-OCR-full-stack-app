import os
import sys
import urllib.request
from pathlib import Path

MODEL_PATH    = os.getenv('ML_MODEL_PATH',    '/app/ml_models/bangla_ocr.keras')
CLASS_MAP     = os.getenv('ML_CLASS_MAP',     '/app/ml_models/class_map.json')
MODEL_URL     = os.getenv('ML_MODEL_URL',     '')
CLASS_MAP_URL = os.getenv('ML_CLASS_MAP_URL', '')

def download_if_missing(url, dest_path, min_size_bytes=1_000):
    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > min_size_bytes:
        print(f"OK (already exists): {dest_path} "
              f"({path.stat().st_size / 1e6:.2f} MB)")
        return

    if not url:
        print(f"ERROR: No URL set for {dest_path}")
        sys.exit(1)

    print(f"Downloading {url}")
    print(f"         -> {dest_path}")
    urllib.request.urlretrieve(url, dest_path)

    actual_size = path.stat().st_size
    print(f"Saved: {actual_size / 1e6:.2f} MB")

    if actual_size < min_size_bytes:
        print(f"ERROR: File too small ({actual_size} bytes). "
              f"Download may be corrupted.")
        path.unlink()   # delete bad file so next deploy retries
        sys.exit(1)

if __name__ == '__main__':
    download_if_missing(MODEL_URL,     MODEL_PATH, min_size_bytes=1_000_000)
    download_if_missing(CLASS_MAP_URL, CLASS_MAP,  min_size_bytes=100)
    print("All model files ready.")