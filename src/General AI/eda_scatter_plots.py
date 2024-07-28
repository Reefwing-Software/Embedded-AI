# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Create subplots for scatter plots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))

# Scatter plot SOC vs Voltage
axes[0, 0].scatter(data['Voltage'], data['SOC'], alpha=0.5, color='lightblue')
axes[0, 0].set_title('SOC vs Voltage')
axes[0, 0].set_xlabel('Voltage')
axes[0, 0].set_ylabel('SOC')
axes[0, 0].grid(True)

# Scatter plot SOC vs Current
axes[0, 1].scatter(data['Current'], data['SOC'], alpha=0.5, color='lightgreen')
axes[0, 1].set_title('SOC vs Current')
axes[0, 1].set_xlabel('Current')
axes[0, 1].set_ylabel('SOC')
axes[0, 1].grid(True)

# Scatter plot Voltage vs Current
axes[0, 2].scatter(data['Voltage'], data['Current'], alpha=0.5, color='lightcoral')
axes[0, 2].set_title('Voltage vs Current')
axes[0, 2].set_xlabel('Voltage')
axes[0, 2].set_ylabel('Current')
axes[0, 2].grid(True)

# Scatter plot SOC vs Average Voltage
axes[1, 0].scatter(data['Average Voltage'], data['SOC'], alpha=0.5, color='lightskyblue')
axes[1, 0].set_title('SOC vs Average Voltage')
axes[1, 0].set_xlabel('Average Voltage')
axes[1, 0].set_ylabel('SOC')
axes[1, 0].grid(True)

# Scatter plot SOC vs Average Current
axes[1, 1].scatter(data['Average Current'], data['SOC'], alpha=0.5, color='lightpink')
axes[1, 1].set_title('SOC vs Average Current')
axes[1, 1].set_xlabel('Average Current')
axes[1, 1].set_ylabel('SOC')
axes[1, 1].grid(True)

# Scatter plot SOC vs Temperature
axes[1, 2].scatter(data['Temperature'], data['SOC'], alpha=0.5, color='lightgoldenrodyellow')
axes[1, 2].set_title('SOC vs Temperature')
axes[1, 2].set_xlabel('Temperature')
axes[1, 2].set_ylabel('SOC')
axes[1, 2].grid(True)

plt.tight_layout()
plt.show()