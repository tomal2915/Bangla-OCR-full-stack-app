import json
import numpy as np
import cv2
import tensorflow as tf
from django.conf import settings

# load model and labels once when Django starts —
# not on every request (that would be very slow)
_model  = None
_labels = None

def get_model():
    global _model, _labels

    if _model is None:
        print("Loading OCR model...")
        _model = tf.keras.models.load_model(str(settings.MODEL_PATH))
        print("Model loaded.")

    if _labels is None:
        with open(settings.LABELS_PATH, 'r', encoding='utf-8') as f:
            _labels = json.load(f)

    return _model, _labels


def predict_character(image_file):
    """
    Takes a Django InMemoryUploadedFile (the uploaded image),
    returns (character, confidence_float).
    """
    model, labels = get_model()

    # read image bytes into numpy array
    file_bytes = np.frombuffer(image_file.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Could not decode image. Make sure it is a valid PNG or JPG.")

    # preprocess — same steps used during training
    img = cv2.resize(img, (32, 32))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=-1)   # (32, 32, 1)
    img = np.expand_dims(img, axis=0)    # (1, 32, 32, 1) — batch dimension

    predictions = model.predict(img, verbose=0)  # shape: (1, 50)

    predicted_idx  = int(np.argmax(predictions[0]))
    confidence     = float(np.max(predictions[0]))
    character      = labels[predicted_idx]

    return character, confidence