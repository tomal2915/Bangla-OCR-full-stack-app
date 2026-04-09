import os
import requests
from pathlib import Path

MODEL_PATH    = os.getenv('ML_MODEL_PATH',    '/app/ml_models/bangla_ocr.h5')
CLASS_MAP     = os.getenv('ML_CLASS_MAP',     '/app/ml_models/class_map.json')
MODEL_URL     = os.getenv('ML_MODEL_URL',     '')
CLASS_MAP_URL = os.getenv('ML_CLASS_MAP_URL', '')

MIN_MODEL_SIZE = 1_000_000   # 1 MB minimum — anything smaller is corrupt

def download_file(url, dest_path, min_size=0):
    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Skip if already valid
    if path.exists() and path.stat().st_size >= min_size:
        print(f"OK (already exists): {dest_path} ({path.stat().st_size / 1e6:.2f} MB)")
        return True

    if not url:
        print(f"ERROR: No URL set for {dest_path}")
        return False

    print(f"Downloading {url}")
    print(f"         → {dest_path}")

    try:
        # stream=True handles large files, allow_redirects follows Cloudinary redirects
        response = requests.get(url, stream=True, allow_redirects=True, timeout=120)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        size = path.stat().st_size
        print(f"Downloaded: {size / 1e6:.2f} MB")

        if size < min_size:
            print(f"ERROR: File too small ({size} bytes) — likely a redirect page, not the model.")
            print(f"First 200 bytes: {path.read_bytes()[:200]}")
            return False

        print(f"OK: {dest_path}")
        return True

    except Exception as e:
        print(f"ERROR downloading {url}: {e}")
        return False

if __name__ == '__main__':
    ok1 = download_file(MODEL_URL,     MODEL_PATH,  min_size=MIN_MODEL_SIZE)
    ok2 = download_file(CLASS_MAP_URL, CLASS_MAP,   min_size=0)

    if not ok1 or not ok2:
        print("FATAL: Model files could not be downloaded. Exiting.")
        raise SystemExit(1)

    print("All model files ready.")