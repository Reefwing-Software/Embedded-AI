# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import tensorflow as tf

# Define the model path
model_save_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/Model")
model_path = os.path.join(model_save_folder, "near_ear_model.keras")

# Load the trained Keras model
model = tf.keras.models.load_model(model_path)

# Define the path to save the model in SavedModel format (ensure this is a directory, not a file path)
saved_model_path = os.path.join(model_save_folder, "saved_near_ear_model_dir")

# Export the model in TensorFlow SavedModel format
model.export(saved_model_path)

print(f"Model successfully converted to SavedModel format and saved to: {saved_model_path}")

# Convert the SavedModel to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
tflite_model_path = os.path.join(model_save_folder, "near_ear_model.tflite")
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)
    
# Print the size of the converted model
basic_model_size = os.path.getsize(tflite_model_path)
print(f"TFLite model saved to {tflite_model_path}")
print(f"Model size: {basic_model_size} bytes")