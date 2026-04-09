import os
import urllib.request
from pathlib import Path

MODEL_PATH    = os.getenv('ML_MODEL_PATH',    '/app/ml_models/bangla_ocr.h5')
CLASS_MAP     = os.getenv('ML_CLASS_MAP',     '/app/ml_models/class_map.json')
MODEL_URL     = os.getenv('ML_MODEL_URL',     '')
CLASS_MAP_URL = os.getenv('ML_CLASS_MAP_URL', '')

def download_if_missing(url, dest_path):
    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 1_000_000:
        print(f"Already exists: {dest_path} ({path.stat().st_size / 1e6:.1f} MB)")
        return

    if not url:
        print(f"ERROR: No URL provided for {dest_path}")
        return

    print(f"Downloading → {dest_path}")
    urllib.request.urlretrieve(url, dest_path)
    size_mb = path.stat().st_size / 1_000_000
    print(f"Done: {size_mb:.1f} MB saved to {dest_path}")

if __name__ == '__main__':
    download_if_missing(MODEL_URL,     MODEL_PATH)
    download_if_missing(CLASS_MAP_URL, CLASS_MAP)
    print("All model files ready.")