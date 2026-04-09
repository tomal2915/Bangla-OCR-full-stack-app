import json
import numpy as np
import tensorflow as tf
from django.conf import settings
from PIL import Image

print("Loading Bangla OCR model...")
model = tf.keras.models.load_model(settings.ML_MODEL_PATH, compile=False)

with open(settings.ML_CLASS_MAP, "r", encoding="utf-8") as f:
    class_map = json.load(f)

print(f"Model loaded from: {settings.ML_MODEL_PATH}")
print(f"Classes loaded: {len(class_map)}")

IMG_SIZE = (32, 32)

def predict_image(image_file):
    img = Image.open(image_file).convert("L")
    img = img.resize(IMG_SIZE)

    arr = np.array(img, dtype="float32") / 255.0
    arr = arr.reshape(1, 32, 32, 1)

    predictions = model.predict(arr, verbose=0)
    class_idx   = int(np.argmax(predictions))
    confidence  = float(np.max(predictions)) * 100

    label = class_map.get(str(class_idx), "Unknown")
    return label, round(confidence, 2)