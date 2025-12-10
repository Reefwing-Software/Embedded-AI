# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import tensorflow as tf
from keras.layers import TFSMLayer

from pathlib import Path

LATENT_DIM = 1000
OUTPUT_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/GAN").expanduser()
MODEL_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_12/GAN").expanduser()
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

def representative_dataset():
    for _ in range(100):
        yield [np.random.normal(0, 1, (1, LATENT_DIM)).astype(np.float32)]

# Load the pre-trained generator model
generator_path = OUTPUT_FOLDER / "generator"
generator = TFSMLayer(generator_path, call_endpoint="serving_default")
generator_model = tf.keras.Sequential([generator])

model_size = os.path.getsize(generator_path)
print(f"Original Generator Model saved at: {generator_path}")
print(f"Model size: {model_size} bytes")

# Fix the input shape for batch size = 1 (for inference)
generator_model.build(input_shape=(1, LATENT_DIM))
print("Generator Model for Inference:")
generator_model.summary()

# Apply Post-Training Quantization (PTQ) for Inference
converter = tf.lite.TFLiteConverter.from_keras_model(generator_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset  
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8  # Quantize input to int8
converter.inference_output_type = tf.int8  # Quantize output to int8
tflite_model = converter.convert()

# Save the quantized TFLite model
model_path = MODEL_FOLDER / "quantized_generator.tflite"
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