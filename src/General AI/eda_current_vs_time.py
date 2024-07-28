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

# Create a time column based on the assumption that each data point is 1 second apart
data['Time'] = data.index

# Plot Current vs Time
plt.figure(figsize=(15, 6))
plt.plot(data['Time'], data['SOC'], color='green', label='SOC')
plt.title('SOC vs Time')
plt.xlabel('Time (seconds)')
plt.ylabel('SOC')
plt.grid(True)
plt.legend()
plt.show()