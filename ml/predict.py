import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import sys

MODEL_PATH    = "ml/bangla_ocr.h5"
CLASS_MAP     = "ml/class_map.json"
IMG_SIZE      = (32, 32)

# Load model and class map
model     = tf.keras.models.load_model(MODEL_PATH)
with open(CLASS_MAP, "r") as f:
    class_map = json.load(f)

def predict(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE,
                         color_mode="grayscale")
    arr = image.img_to_array(img) / 255.0   # normalize
    arr = np.expand_dims(arr, axis=0)        # add batch dimension

    predictions = model.predict(arr)
    class_idx   = int(np.argmax(predictions))
    confidence  = float(np.max(predictions)) * 100

    print(f"Predicted class : {class_map[str(class_idx)]}")
    print(f"Confidence      : {confidence:.2f}%")

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "test.png"
    predict(img_path)

    
# ```

# Test it with any handwritten character image:
# ```
# python ml/predict.py path\to\your\image.png