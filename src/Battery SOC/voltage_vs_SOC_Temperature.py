# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

# Define the file path
train_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Train")

# Function to read .mat files
def read_mat_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            data.append(mat_data)
    return data

# Load the training data
fds_train = read_mat_files(train_folder)
train_data_full = fds_train[0]

# Extract X and Y from train_data_full
X = train_data_full['X']
Y = train_data_full['Y']

# Define the index ranges
idx0 = slice(0, 184257)    # Temperature = 0°C
idx10 = slice(184257, 337973)    # Temperature = 10°C
idx25 = slice(337973, 510530)    # Temperature = 25°C
idxN10 = slice(510530, 669956)    # Temperature = -10°C

# Extract data segments
X_idx0 = X[:, idx0]
Y_idx0 = Y[:, idx0]

X_idx10 = X[:, idx10]
Y_idx10 = Y[:, idx10]

X_idx25 = X[:, idx25]
Y_idx25 = Y[:, idx25]

X_idxN10 = X[:, idxN10]
Y_idxN10 = Y[:, idxN10]

# Plotting Voltage vs SOC for different temperature bands
plt.figure(figsize=(10, 6))

# 0°C
plt.plot(Y_idx0.flatten(), X_idx0[0, :], label='0°C', color='blue')

# 10°C
plt.plot(Y_idx10.flatten(), X_idx10[0, :], label='10°C', color='orange')

# 25°C
plt.plot(Y_idx25.flatten(), X_idx25[0, :], label='25°C', color='green')

# -10°C
plt.plot(Y_idxN10.flatten(), X_idxN10[0, :], label='-10°C', color='red')

plt.xlabel('State of Charge (SOC)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs SOC over Multiple Cycles for Different Temperatures')
plt.gca().invert_xaxis()  # Invert the x-axis
plt.legend()
plt.grid(True)
plt.show()