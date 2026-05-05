# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import tensorflow.lite as tflite
from pathlib import Path
import numpy as np

MODEL_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_11/GAN").expanduser()
model_path = MODEL_FOLDER / "quantized_generator.tflite"

interpreter = tflite.Interpreter(model_path=str(model_path))
interpreter.allocate_tensors()

tensor_details = interpreter.get_tensor_details()
total_tensor_size = 0

for t in tensor_details:
    if 'shape' in t and 'dtype' in t:
        num_elements = np.prod(t['shape'])
        
        # Handle different data types and potential XNNPACK quantization
        if t['dtype'] == np.float32:
            element_size = 4  # float32 is 4 bytes
        elif t['dtype'] == np.int8 or t['dtype'] == np.uint8:
            element_size = 1  # int8 and uint8 are 1 byte
        elif t['dtype'] == np.int32:
            element_size = 4 # int32 is 4 bytes
        elif t['dtype'] == np.int64:
            element_size = 8 # int64 is 8 bytes
        else:
            print(f"Warning: Unhandled data type {t['dtype']} for tensor: {t}")
            element_size = 0  # Default to 0 if unknown
            
        total_tensor_size += num_elements * element_size
    else:
        print(f"Warning: Could not determine size for tensor: {t}")

recommended_size = total_tensor_size + 1024
print(f"Recommended kTensorArenaSize: {recommended_size} bytes")