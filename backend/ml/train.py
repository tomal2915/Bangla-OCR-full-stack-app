import json
import tensorflow as tf
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)
from dataset import load_dataset
from model import build_model

EPOCHS     = 50
BATCH_SIZE = 32

def train():
    X_train, X_val, y_train, y_val, class_names = load_dataset()
    num_classes = len(class_names)
    print(f"Training with {num_classes} classes")

    model = build_model(num_classes)
    model.summary()

    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath='../bangla_ocr_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-6,
            verbose=1
        ),
    ]

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )

    # save model
    model.save('../bangla_ocr.h5')
    print("Model saved → bangla_ocr.h5")

    # save class labels — Django will use this to decode predictions
    with open('../class_labels.json', 'w', encoding='utf-8') as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)
    print("Labels saved → class_labels.json")

    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\nFinal validation accuracy: {val_acc:.4f} ({val_acc*100:.1f}%)")


if __name__ == '__main__':
    train()