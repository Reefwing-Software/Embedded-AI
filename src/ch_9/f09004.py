# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09004.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file names
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_9")
file_r1 = "beta_optimizationR1.txt"
file_r2 = "beta_optimizationR2.txt"
file_path_r1 = os.path.join(data_folder, file_r1)
file_path_r2 = os.path.join(data_folder, file_r2)

# Function to read data from a file
def read_data(file_path):
    beta = []
    rms_error = []
    with open(file_path, 'r') as file:
        # Skip the header row
        next(file)
        for line in file:
            values = line.strip().split()
            if len(values) == 2:
                beta.append(float(values[0]))
                rms_error.append(float(values[1]))
    return beta, rms_error

# Read data from both files
beta_r1, rms_error_r1 = read_data(file_path_r1)
beta_r2, rms_error_r2 = read_data(file_path_r2)

# Find the optimum beta and corresponding RMS error for both datasets
optimum_index_r1 = rms_error_r1.index(min(rms_error_r1))
optimum_beta_r1 = beta_r1[optimum_index_r1]
optimum_error_r1 = rms_error_r1[optimum_index_r1]

optimum_index_r2 = rms_error_r2.index(min(rms_error_r2))
optimum_beta_r2 = beta_r2[optimum_index_r2]
optimum_error_r2 = rms_error_r2[optimum_index_r2]

# Create the plots
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Plot for Nano 33 BLE Rev 1
axes[0].plot(beta_r1, rms_error_r1, color="black", linewidth=1.5, label="RMS error")
axes[0].scatter(optimum_beta_r1, optimum_error_r1, color="grey", label=f"Optimum beta = {optimum_beta_r1:.2f}\nMinimium error = {optimum_error_r1:.2f}", zorder=5)
axes[0].grid(color="gray", linestyle="--", linewidth=0.5)
axes[0].set_xlabel("Beta", fontproperties=prop)
axes[0].set_ylabel("Static RMS error", fontproperties=prop)
axes[0].set_title("Nano 33 BLE Rev 1 (LSM9DS1)", fontproperties=prop)
axes[0].legend(prop=prop, loc="upper right")

# Plot for Nano 33 BLE Rev 2
axes[1].plot(beta_r2, rms_error_r2, color="black", linewidth=1.5, label="RMS error")
axes[1].scatter(optimum_beta_r2, optimum_error_r2, color="grey", label=f"Optimum beta = {optimum_beta_r2:.2f}\nMinimum error = {optimum_error_r2:.2f}", zorder=5)
axes[1].grid(color="gray", linestyle="--", linewidth=0.5)
axes[1].set_xlabel("Beta", fontproperties=prop)
axes[1].set_title("Nano 33 BLE Rev 2 (BMI270)", fontproperties=prop)
axes[1].legend(prop=prop, loc="upper right")

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()