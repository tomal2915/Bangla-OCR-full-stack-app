import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent / '.env')

cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key    = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET'),
)

# Upload model
print("Uploading bangla_ocr.h5 ... (may take 1-2 mins on slow internet)")
r1 = cloudinary.uploader.upload(
    "ml/bangla_ocr.h5",
    resource_type = "raw",
    public_id     = "bangla_ocr_model",
    overwrite     = True,
)
print(f"Model URL: {r1['secure_url']}")

# Upload class map
print("Uploading class_map.json ...")
r2 = cloudinary.uploader.upload(
    "ml/class_map.json",
    resource_type = "raw",
    public_id     = "class_map",
    overwrite     = True,
)
print(f"Class map URL: {r2['secure_url']}")