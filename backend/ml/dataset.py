import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from label_map import LABEL_MAP

IMG_SIZE    = 32
# use the folder where dataset.py lives, then go up one level to backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets')

def load_dataset():
    images = []
    labels = []
    class_names = []  # ordered list of Bangla characters

    # only load folders that exist in LABEL_MAP
    valid_folders = sorted(
        [f for f in os.listdir(DATASET_PATH) if f in LABEL_MAP],
        key=lambda x: int(x)
    )

    if not valid_folders:
        raise ValueError(
            f"No valid folders found in '{DATASET_PATH}'. "
            f"Expected folders like 172, 173, ... 221"
        )

    # build an ordered class list: [অ, আ, ই, ...]
    class_names = [LABEL_MAP[f] for f in valid_folders]
    print(f"Found {len(class_names)} classes: {class_names}")

    for label_idx, folder_name in enumerate(valid_folders):
        folder_path = os.path.join(DATASET_PATH, folder_name)

        img_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]

        if not img_files:
            print(f"  Warning: no images in folder {folder_name}, skipping.")
            continue

        for img_file in img_files:
            img_path = os.path.join(folder_path, img_file)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.astype('float32') / 255.0
            img = np.expand_dims(img, axis=-1)  # (32, 32, 1)

            images.append(img)
            labels.append(label_idx)

    if not images:
        raise ValueError("No images were loaded. Check your datasets/ folder.")

    images = np.array(images)
    labels = np.array(labels)

    labels_onehot = to_categorical(labels, num_classes=len(class_names))

    X_train, X_val, y_train, y_val = train_test_split(
        images, labels_onehot,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    print(f"Training samples  : {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    return X_train, X_val, y_train, y_val, class_names