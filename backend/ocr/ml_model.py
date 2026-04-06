import json
import os
import numpy as np
from django.conf import settings
from PIL import Image

BANGLA_CHAR_MAP = {
    "0":  "০", "1":  "১", "2":  "২", "3":  "৩", "4":  "৪",
    "5":  "৫", "6":  "৬", "7":  "৭", "8":  "৮", "9":  "৯",
    "10": "ক", "11": "খ", "12": "গ", "13": "ঘ", "14": "ঙ",
    "15": "চ", "16": "ছ", "17": "জ", "18": "ঝ", "19": "ঞ",
    "20": "ট", "21": "ঠ", "22": "ড", "23": "ঢ", "24": "ণ",
    "25": "ত", "26": "থ", "27": "দ", "28": "ধ", "29": "ন",
    "30": "প", "31": "ফ", "32": "ব", "33": "ভ", "34": "ম",
    "35": "য", "36": "র", "37": "ল", "38": "শ", "39": "ষ",
    "40": "স", "41": "হ", "42": "ড়", "43": "ঢ়", "44": "য়",
    "45": "ৎ", "46": "ং", "47": "ঃ", "48": "ঁ", "49": "্",
}

model     = None
class_map = {}
IMG_SIZE  = (32, 32)

def _load():
    global model, class_map

    model_path    = settings.ML_MODEL_PATH
    class_map_path = settings.ML_CLASS_MAP

    if not os.path.exists(model_path):
        print(f"WARNING: Model not found at {model_path} — prediction disabled.")
        return

    if not os.path.exists(class_map_path):
        print(f"WARNING: Class map not found at {class_map_path} — prediction disabled.")
        return

    import tensorflow as tf
    print("Loading Bangla OCR model...")
    model = tf.keras.models.load_model(model_path)
    with open(class_map_path, "r", encoding="utf-8") as f:
        class_map = json.load(f)
    print("Model loaded successfully.")

_load()   # runs once when Django starts

def predict_image(image_file):
    if model is None:
        raise RuntimeError(
            "ML model is not loaded on this server. "
            "Please configure ML_MODEL_PATH and ML_CLASS_MAP correctly."
        )

    img = Image.open(image_file).convert("L")
    img = img.resize(IMG_SIZE)

    arr = np.array(img, dtype="float32") / 255.0
    arr = arr.reshape(1, 32, 32, 1)

    predictions = model.predict(arr, verbose=0)
    class_idx   = int(np.argmax(predictions))
    confidence  = float(np.max(predictions)) * 100

    folder_name = class_map.get(str(class_idx), str(class_idx))
    label       = BANGLA_CHAR_MAP.get(folder_name, folder_name)

    return label, round(confidence, 2)