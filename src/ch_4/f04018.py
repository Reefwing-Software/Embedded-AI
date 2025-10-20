# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04018.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder
train_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC/Train")

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
idx0 = slice(0, 184257)         # Temperature = 0°C
idx10 = slice(184257, 337973)   # Temperature = 10°C
idx25 = slice(337973, 510530)   # Temperature = 25°C
idxN10 = slice(510530, 669956)  # Temperature = -10°C

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
plt.plot(Y_idx0.flatten(), X_idx0[0, :], label='0°C', color='black', linestyle='-')

# 10°C
plt.plot(Y_idx10.flatten(), X_idx10[0, :], label='10°C', color='grey', linestyle='--')

# 25°C
plt.plot(Y_idx25.flatten(), X_idx25[0, :], label='25°C', color='darkgrey', linestyle='-.')

# -10°C
plt.plot(Y_idxN10.flatten(), X_idxN10[0, :], label='-10°C', color='lightgrey', linestyle=':')

# Apply font properties
plt.xlabel('State of charge (SOC)', fontproperties=prop)
plt.ylabel('Voltage (V)', fontproperties=prop)
# plt.title('Voltage vs SOC over Multiple Cycles', fontproperties=prop)
plt.gca().invert_xaxis()  # Invert the x-axis
plt.legend(prop=prop)
plt.grid(True, linestyle='--', linewidth=0.5)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()