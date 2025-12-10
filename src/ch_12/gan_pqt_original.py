# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import tensorflow as tf

from pathlib import Path

OUTPUT_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/GAN").expanduser()
MODEL_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_12/GAN").expanduser()
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

# Apply Post-Training Quantization (PTQ) for Inference
generator_path = OUTPUT_FOLDER / "generator"
converter = tf.lite.TFLiteConverter.from_saved_model(str(generator_path))
tflite_model = converter.convert()

# Save the quantized TFLite model
model_path = MODEL_FOLDER / "generator.tflite"
with open(model_path, "wb") as f:
    f.write(tflite_model)

model_size = os.path.getsize(model_path)
print(f"Quantized Generator Model saved at: {model_path}")
print(f"Model size: {model_size} bytes")

# Load the quantized TFLite model to inspect its details
interpreter = tf.lite.Interpreter(model_path=str(model_path))
interpreter.allocate_tensors()

print("Quantized Generator Model Summary:")
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input details:", input_details)
print("Output details:", output_details)
