import tensorflow as tf

print("Loading old model...")
model = tf.keras.models.load_model('ml/bangla_ocr.h5')

print("Saving in new .keras format...")
model.save('ml/bangla_ocr.keras')

print("Done. New file: ml/bangla_ocr.keras")