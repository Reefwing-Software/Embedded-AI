# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import scipy.io
import pandas as pd
import numpy as np

def read_mat_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            data.append(mat_data)
    return data

# Resample and compute new moving averages
def resample_and_compute_moving_averages(X, Y, step=100):
    # Resample the data (take every `step`-th point)
    X_resampled = X[:, ::step]
    Y_resampled = Y[:, ::step]
    
    # Compute new moving averages
    n = X_resampled.shape[1]
    avg_voltage_idx = 3  # The 4th row (index 3) is average voltage
    avg_current_idx = 4  # The 5th row (index 4) is average current
    
    new_avg_voltage = np.empty(n)
    new_avg_current = np.empty(n)
    
    for i in range(n):
        new_avg_voltage[i] = np.mean(X_resampled[0, max(0, i-5):i+1])
        new_avg_current[i] = np.mean(X_resampled[1, max(0, i-5):i+1])
    
    X_resampled[avg_voltage_idx, :n] = new_avg_voltage
    X_resampled[avg_current_idx, :n] = new_avg_current
    
    return X_resampled, Y_resampled

# Folder paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC")
train_folder = os.path.join(data_folder, "Train")
test_folder = os.path.join(data_folder, "Test")
preprocessed_folder = os.path.join(data_folder, 'Preprocessed')
os.makedirs(preprocessed_folder, exist_ok=True)

# Create a file datastore for both the training data and the test data
fds_train = read_mat_files(train_folder)
fds_test = read_mat_files(test_folder)
train_data_full = fds_train[0]

# Extract X and Y from train_data_full
X_train = train_data_full['X']
Y_train = train_data_full['Y']

# Resample and compute new moving averages for training data
X_train_resampled, Y_train_resampled = resample_and_compute_moving_averages(X_train, Y_train)

# Create DataFrame and save to CSV
train_df = pd.DataFrame(np.vstack((X_train_resampled, Y_train_resampled)).T,
                        columns=['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC'])
train_df.to_csv(os.path.join(preprocessed_folder, 'resampled_training_data.csv'), index=False)

# Extract and resample test data
test_data_files = ['n10degC', '0degC', '10degC', '25degC']
resampled_test_data_shapes = {}

for i, test_data_full in enumerate(fds_test):
    X_test = test_data_full['X']
    Y_test = test_data_full['Y']
    X_test_resampled, Y_test_resampled = resample_and_compute_moving_averages(X_test, Y_test)
    test_df = pd.DataFrame(np.vstack((X_test_resampled, Y_test_resampled)).T,
                           columns=['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC'])
    test_df.to_csv(os.path.join(preprocessed_folder, f'resampled_test_data_{test_data_files[i]}.csv'), index=False)
    resampled_test_data_shapes[test_data_files[i]] = (X_test_resampled.shape, Y_test_resampled.shape)

# Print shapes to verify resampling
print(f'Training data shape after resampling: X={X_train_resampled.shape}, Y={Y_train_resampled.shape}')
for test_file, shapes in resampled_test_data_shapes.items():
    print(f'{test_file} test data shape after resampling: X={shapes[0]}, Y={shapes[1]}')

# Combine X and Y into a single DataFrame
data_resampled = np.vstack((X_train_resampled, Y_train_resampled))
df_resampled = pd.DataFrame(data_resampled.T, columns=['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC'])

# Display the first 8 rows
print(df_resampled.head(8).to_string(index=False))