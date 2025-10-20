# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import scipy.io

def read_mat_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            data.append(mat_data)
    return data

# Folder paths
train_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC/Train")
test_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC/Test")

# Create a file datastore for both the training data and the test data
fds_train = read_mat_files(train_folder)
fds_test = read_mat_files(test_folder)

# Read all data in the datastores
train_data_full = fds_train[0]

# Extract X and Y from train_data_full
X = train_data_full['X']
Y = train_data_full['Y']

# Define the index ranges
idx0 = slice(0, 184257)
idx10 = slice(184257, 337973)
idx25 = slice(337973, 510530)
idxN10 = slice(510530, 669956)

# Extract data segments
X_idx0 = X[:, idx0]
Y_idx0 = Y[:, idx0]

X_idx10 = X[:, idx10]
Y_idx10 = Y[:, idx10]

X_idx25 = X[:, idx25]
Y_idx25 = Y[:, idx25]

X_idxN10 = X[:, idxN10]
Y_idxN10 = Y[:, idxN10]

# Print shapes to verify extraction
print(f'X_idx0 shape: {X_idx0.shape}, Y_idx0 shape: {Y_idx0.shape}')
print(f'X_idx10 shape: {X_idx10.shape}, Y_idx10 shape: {Y_idx10.shape}')
print(f'X_idx25 shape: {X_idx25.shape}, Y_idx25 shape: {Y_idx25.shape}')
print(f'X_idxN10 shape: {X_idxN10.shape}, Y_idxN10 shape: {Y_idxN10.shape}')