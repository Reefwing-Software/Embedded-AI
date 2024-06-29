# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import requests
import zipfile
import scipy.io
import pandas as pd
import numpy as np

# URL of the file to download
url = "https://data.mendeley.com/public-files/datasets/cp3473x7xv/files/ad7ac5c9-2b9e-458a-a91f-6f3da449bdfb/file_downloaded"

# Output folder contains the extracted ZIP files
output_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC")
os.makedirs(output_folder, exist_ok=True)

# Download and extract the data set
train_folder = os.path.join(output_folder, "Train")
test_folder = os.path.join(output_folder, "Test")
if not os.path.exists(train_folder) or not os.path.exists(test_folder):
    print("Downloading LGHG2@n10C_to_25degC.zip (56 MB) ... ")
    download_folder = os.path.dirname(output_folder)
    filename = os.path.join(download_folder, "LGHG2@n10C_to_25degC.zip")
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

# Define helper function to read .mat files
def read_mat_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            data.append(mat_data)
    return data

# Create a file datastore for both the training data and the test data
fds_train = read_mat_files(train_folder)
fds_test = read_mat_files(test_folder)

# Read all data in the datastores
train_data_full = fds_train[0]
test_data_full_n10deg = fds_test[0]
test_data_full_0deg = fds_test[1]
test_data_full_10deg = fds_test[2]
test_data_full_25deg = fds_test[3]

# Print the shapes of the data arrays to understand their structure
print("Shape of train_data_full['X']: ", train_data_full['X'].shape)
print("Shape of train_data_full['Y']: ", train_data_full['Y'].shape)
print("Shape of test_data_full_n10deg['X']: ", test_data_full_n10deg['X'].shape)
print("Shape of test_data_full_n10deg['Y']: ", test_data_full_n10deg['Y'].shape)

# Extract X and Y from train_data_full
X_train = train_data_full['X']
Y_train = train_data_full['Y']

# Define the index ranges
idx0 = slice(0, 184257)
idx10 = slice(184257, 337973)
idx25 = slice(337973, 510530)
idxN10 = slice(510530, 669956)

# Extract data segments
X_idx0 = X_train[:, idx0]
Y_idx0 = Y_train[:, idx0]

X_idx10 = X_train[:, idx10]
Y_idx10 = Y_train[:, idx10]

X_idx25 = X_train[:, idx25]
Y_idx25 = Y_train[:, idx25]

X_idxN10 = X_train[:, idxN10]
Y_idxN10 = Y_train[:, idxN10]

# Print shapes to verify extraction
print(f'X_idx0 shape: {X_idx0.shape}, Y_idx0 shape: {Y_idx0.shape}')
print(f'X_idx10 shape: {X_idx10.shape}, Y_idx10 shape: {Y_idx10.shape}')
print(f'X_idx25 shape: {X_idx25.shape}, Y_idx25 shape: {Y_idx25.shape}')
print(f'X_idxN10 shape: {X_idxN10.shape}, Y_idxN10 shape: {Y_idxN10.shape}')

# Resample and compute new moving averages
def resample_and_compute_moving_averages(X, Y, step=100):
    # Resample the data (take every `step`-th point)
    X_resampled = X[:, ::step]
    Y_resampled = Y[:, ::step]
    
    # Compute new moving averages
    avg_voltage_idx = 3  # The 4th row (index 3) is average voltage
    avg_current_idx = 4  # The 5th row (index 4) is average current
    
    # Use a simple moving average (window size = step)
    new_avg_voltage = np.convolve(X_resampled[0, :], np.ones(step)/step, mode='valid')
    new_avg_current = np.convolve(X_resampled[1, :], np.ones(step)/step, mode='valid')
    
    # Update the resampled X with new moving averages
    X_resampled[avg_voltage_idx, :len(new_avg_voltage)] = new_avg_voltage
    X_resampled[avg_current_idx, :len(new_avg_current)] = new_avg_current
    
    return X_resampled, Y_resampled


# Resample and compute new moving averages for training data
X_train_resampled, Y_train_resampled = resample_and_compute_moving_averages(X_train, Y_train)

# Extract and resample test data
X_test_n10deg = test_data_full_n10deg['X']
Y_test_n10deg = test_data_full_n10deg['Y']
X_test_n10deg_resampled, Y_test_n10deg_resampled = resample_and_compute_moving_averages(X_test_n10deg, Y_test_n10deg)

X_test_0deg = test_data_full_0deg['X']
Y_test_0deg = test_data_full_0deg['Y']
X_test_0deg_resampled, Y_test_0deg_resampled = resample_and_compute_moving_averages(X_test_0deg, Y_test_0deg)

X_test_10deg = test_data_full_10deg['X']
Y_test_10deg = test_data_full_10deg['Y']
X_test_10deg_resampled, Y_test_10deg_resampled = resample_and_compute_moving_averages(X_test_10deg, Y_test_10deg)

X_test_25deg = test_data_full_25deg['X']
Y_test_25deg = test_data_full_25deg['Y']
X_test_25deg_resampled, Y_test_25deg_resampled = resample_and_compute_moving_averages(X_test_25deg, Y_test_25deg)

# Print shapes to verify resampling
print(f'Training data shape after resampling: X={X_train_resampled.shape}, Y={Y_train_resampled.shape}')
print(f'n10degC test data shape after resampling: X={X_test_n10deg_resampled.shape}, Y={Y_test_n10deg_resampled.shape}')
print(f'0degC test data shape after resampling: X={X_test_0deg_resampled.shape}, Y={Y_test_0deg_resampled.shape}')
print(f'10degC test data shape after resampling: X={X_test_10deg_resampled.shape}, Y={Y_test_10deg_resampled.shape}')
print(f'25degC test data shape after resampling: X={X_test_25deg_resampled.shape}, Y={Y_test_25deg_resampled.shape}')