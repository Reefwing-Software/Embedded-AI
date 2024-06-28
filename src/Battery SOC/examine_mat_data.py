# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import scipy.io
import numpy as np

# Define helper function to read and print first 10 lines of .mat file contents
def read_and_print_mat_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            print(f"Contents of {filename}:")
            for key in mat_data:
                if not key.startswith("__"):
                    data = mat_data[key]
                    if isinstance(data, np.ndarray) and data.ndim > 1:  # Check if data is a multi-dimensional array
                        print(f"{key}:")
                        print(data[:10])  # Print first 10 lines of data
                    else:
                        print(f"{key}: {data}")
            print("\n")

# Folder paths
train_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Train")
test_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Test")

# Read and print contents of Train and Test files
print("Training Data Files:")
read_and_print_mat_files(train_folder)
print("\nTest Data Files:")
read_and_print_mat_files(test_folder)