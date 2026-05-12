# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np

# Define data folder and file paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_12/")
X_file = os.path.join(data_folder, "ei-hello-world-syntiant-X_training.npy")
y_file = os.path.join(data_folder, "ei-hello-world-syntiant-y_training.npy")

# Function to load and display .npy file data
def inspect_npy_file(file_path, file_description):
    print(f"--- Inspecting {file_description} ---")
    # Load the file
    data = np.load(file_path)
    
    # Print metadata
    print(f"Shape: {data.shape}")
    print(f"Data Type: {data.dtype}")
    
    # Print data (only a subset if large)
    print("Data Preview:")
    if data.size > 100:  # Avoid printing huge arrays
        print(data[:10])  # Print first 10 rows
        print("... [Data truncated: showing first 10 rows only]")
    else:
        print(data)
    print("\n")

# Inspect both files
inspect_npy_file(X_file, "X_training.npy (Input Data)")
inspect_npy_file(y_file, "y_training.npy (Labels)")