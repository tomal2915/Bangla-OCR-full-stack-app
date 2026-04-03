import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt

# ── Config ────────────────────────────────────────────────
DATASET_DIR = "ml/dataset"
MODEL_PATH   = "ml/bangla_ocr.h5"
IMG_SIZE     = (32, 32)
BATCH_SIZE   = 32
EPOCHS       = 30
NUM_CLASSES  = 50          # CMATERdb has 50 Bangla character classes

# ── Data loading & augmentation ───────────────────────────
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,        # normalize pixels to 0-1
    validation_split=0.2,     # 80% train, 20% validation
    rotation_range=10,        # slight rotation for variety
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    color_mode="grayscale",   # Bangla chars don't need color
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True,
)

val_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
)

# ── CNN Model ─────────────────────────────────────────────
def build_model(num_classes):
    model = models.Sequential([

        # Explicit input layer (recommended for Keras 3+)
        layers.Input(shape=(32, 32, 1)),

        # Block 1 — detect simple edges and curves
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Block 2 — detect more complex shapes
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Block 3 — high-level character features
        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Classifier head
        layers.Flatten(),
        layers.Dense(256, activation="relu"),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ])
    return model

model = build_model(NUM_CLASSES)
model.summary()

# ── Compile ───────────────────────────────────────────────
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# ── Callbacks ─────────────────────────────────────────────
callbacks = [
    # Save the best model automatically during training
    ModelCheckpoint(MODEL_PATH, save_best_only=True,
                    monitor="val_accuracy", verbose=1),
    # Stop early if validation accuracy stops improving
    EarlyStopping(monitor="val_accuracy", patience=5,
                  restore_best_weights=True, verbose=1),
]

# ── Train ─────────────────────────────────────────────────
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks,
)

# ── Plot accuracy & loss ──────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(history.history["accuracy"],     label="Train accuracy")
ax1.plot(history.history["val_accuracy"], label="Val accuracy")
ax1.set_title("Accuracy")
ax1.legend()

ax2.plot(history.history["loss"],     label="Train loss")
ax2.plot(history.history["val_loss"], label="Val loss")
ax2.set_title("Loss")
ax2.legend()

plt.tight_layout()
plt.savefig("ml/training_curves.png")
print("Training curves saved to ml/training_curves.png")

# Save class index mapping (needed by Django later)
import json
class_indices = train_gen.class_indices
class_map = {v: k for k, v in class_indices.items()}  # {0: 'label', ...}
with open("ml/class_map.json", "w") as f:
    json.dump(class_map, f, ensure_ascii=False)
print("Class map saved to ml/class_map.json")
print(f"\nDone. Model saved to {MODEL_PATH}")


# ```

# ---

# ## Step 3 — Run the training

# Make sure your venv is active, then from the root project folder:
# ```
# python ml/train.py
# ```

# You'll see output like this per epoch:
# ```
# Epoch 1/30
# 300/300 ━━━━━━━━━━━━━━━━━━━━ 12s - accuracy: 0.42 - val_accuracy: 0.61
# Epoch 2/30
# 300/300 ━━━━━━━━━━━━━━━━━━━━ 10s - accuracy: 0.67 - val_accuracy: 0.74
# ...