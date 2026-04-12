import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)
from dataset import load_dataset
from model import build_model

EPOCHS     = 50    # max epochs (early stopping will kick in sooner)
BATCH_SIZE = 32

def train():
    # 1. load data
    X_train, X_val, y_train, y_val, classes = load_dataset()
    num_classes = len(classes)

    # 2. build model
    model = build_model(num_classes)
    model.summary()

    # 3. callbacks
    callbacks = [
        # stop training if val_accuracy doesn't improve for 8 epochs
        EarlyStopping(
            monitor='val_accuracy',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),
        # save the best model automatically during training
        ModelCheckpoint(
            filepath='../bangla_ocr_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        # reduce learning rate when training plateaus
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-6,
            verbose=1
        ),
    ]

    # 4. train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )

    # 5. save final model
    model.save('../bangla_ocr.h5')
    print("Model saved → bangla_ocr.h5")

    # 6. save class labels so Django knows which index = which character
    with open('../class_labels.json', 'w', encoding='utf-8') as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    print("Labels saved → class_labels.json")

    # 7. print final accuracy
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\nFinal validation accuracy: {val_acc:.4f} ({val_acc*100:.1f}%)")


if __name__ == '__main__':
    train()