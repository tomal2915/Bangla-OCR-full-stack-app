import json
import numpy as np
import tensorflow as tf
from django.conf import settings
from PIL import Image

# Bangla character map (keep as is)
BANGLA_CHAR_MAP = {
    "0": "০", "1": "১", "2": "২", "3": "৩", "4": "৪",
    "5": "৫", "6": "৬", "7": "৭", "8": "৮", "9": "৯",
    "10": "ক", "11": "খ", "12": "গ", "13": "ঘ", "14": "ঙ",
    "15": "চ", "16": "ছ", "17": "জ", "18": "ঝ", "19": "ঞ",
    "20": "ট", "21": "ঠ", "22": "ড", "23": "ঢ", "24": "ণ",
    "25": "ত", "26": "থ", "27": "দ", "28": "ধ", "29": "ন",
    "30": "প", "31": "ফ", "32": "ব", "33": "ভ", "34": "ম",
    "35": "য", "36": "র", "37": "ল", "38": "শ", "39": "ষ",
    "40": "স", "41": "হ", "42": "ড়", "43": "ঢ়", "44": "য়",
    "45": "ৎ", "46": "ং", "47": "ঃ", "48": "ঁ", "49": "্",
}

IMG_SIZE = (32, 32)

# Global variables (initialized as None)
_model = None
_class_map = None

def _load_model_and_map():
    """Load model and class map once, cache globally."""
    global _model, _class_map
    if _model is None:
        print("Loading Bangla OCR model...")
        _model = tf.keras.models.load_model(settings.ML_MODEL_PATH)
        print("Model loaded.")
    if _class_map is None:
        with open(settings.ML_CLASS_MAP, "r", encoding="utf-8") as f:
            _class_map = json.load(f)
        print("Class map loaded.")
    return _model, _class_map

def predict_image(image_file):
    # Load model & map only on first call (not at startup)
    model, class_map = _load_model_and_map()

    img = Image.open(image_file).convert("L")
    img = img.resize(IMG_SIZE)

    arr = np.array(img, dtype="float32") / 255.0
    arr = arr.reshape(1, 32, 32, 1)

    predictions = model.predict(arr, verbose=0)
    class_idx = int(np.argmax(predictions))
    confidence = float(np.max(predictions)) * 100

    folder_name = class_map.get(str(class_idx), str(class_idx))
    label = BANGLA_CHAR_MAP.get(folder_name, folder_name)

    return label, round(confidence, 2)