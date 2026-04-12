import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

IMG_SIZE = 32   # resize all images to 32×32
# use the folder where dataset.py lives, then go up one level to backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets')

def load_dataset():
    images = []
    labels = []

    # get sorted list of class folders (each folder = one character)
    classes = sorted(os.listdir(DATASET_PATH))
    num_classes = len(classes)
    print(f"Found {num_classes} classes: {classes}")

    for label_idx, class_name in enumerate(classes):
        class_folder = os.path.join(DATASET_PATH, class_name)

        if not os.path.isdir(class_folder):
            continue

        for img_file in os.listdir(class_folder):
            img_path = os.path.join(class_folder, img_file)

            # read as grayscale
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            # resize to 32×32
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            # normalize pixel values from 0–255 to 0.0–1.0
            img = img.astype('float32') / 255.0

            # add channel dimension → (32, 32, 1)
            img = np.expand_dims(img, axis=-1)

            images.append(img)
            labels.append(label_idx)

    images = np.array(images)
    labels = np.array(labels)

    # one-hot encode labels → [0,1,0,...] instead of 2
    labels_onehot = to_categorical(labels, num_classes=num_classes)

    # 80% train, 20% validation split
    X_train, X_val, y_train, y_val = train_test_split(
        images, labels_onehot,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    print(f"Training samples  : {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    return X_train, X_val, y_train, y_val, classes