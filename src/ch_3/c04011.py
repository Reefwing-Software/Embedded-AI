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
test_data_full_n10deg = fds_test[0]
test_data_full_0deg = fds_test[1]
test_data_full_10deg = fds_test[2]
test_data_full_25deg = fds_test[3]

# Print the shapes of the data arrays to understand their structure
print("Shape of train_data_full['X']: ", train_data_full['X'].shape)
print("Shape of train_data_full['Y']: ", train_data_full['Y'].shape)
print("Shape of test_data_full_n10deg['X']: ", test_data_full_n10deg['X'].shape)
print("Shape of test_data_full_n10deg['Y']: ", test_data_full_n10deg['Y'].shape)